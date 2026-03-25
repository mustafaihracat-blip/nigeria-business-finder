"""
Ana iş mantığı - NigeriaBusinessFinder
"""

import sys
import os
import time
import random
import logging
import pandas as pd
from datetime import datetime
from tqdm import tqdm

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

logger = logging.getLogger(__name__)


class NigeriaBusinessFinder:
    def __init__(self, product_group: str, regions: list = None, scrape_details: bool = True):
        """
        Args:
            product_group : Aranacak ürün/sektör (ör: "solar panels", "cement")
            regions       : Sadece belirli bölgeler; None = tüm Nijerya
            scrape_details: Firma sitelerini ziyaret edip iletişim bilgisi çeksin mi?
        """
        from data.nigeria_regions import NIGERIA_REGIONS, ALL_CITIES
        from src.scraper import search_all, scrape_company_details

        self.product_group   = product_group
        self.scrape_details  = scrape_details
        self._search         = search_all
        self._scrape_detail  = scrape_company_details
        self.results         = []

        self.cities = [c for c in ALL_CITIES if (not regions or c["region"] in regions)]

        logger.info(f"🔍 Ürün grubu : {product_group}")
        logger.info(f"📍 Toplam şehir: {len(self.cities)}")

    # ------------------------------------------------------------------
    def _build_queries(self, city: str) -> list:
        pg = self.product_group
        return [
            f"{pg} companies in {city} Nigeria",
            f"{pg} suppliers {city} Nigeria",
            f"best {pg} distributors {city} Nigeria",
            f"{pg} wholesalers {city} Nigeria contact",
        ]

    # ------------------------------------------------------------------
    def _search_city(self, city_info: dict) -> list:
        city, region = city_info["city"], city_info["region"]
        city_results, seen_links = [], set()

        for query in self._build_queries(city)[:2]:   # ilk 2 sorgu
            for result in self._search(query, num_results=8):
                link = result.get("link", "")
                if not link or link in seen_links:
                    continue
                seen_links.add(link)

                entry = {
                    "company_name" : result["title"],
                    "city"         : city,
                    "region"       : region,
                    "product_group": self.product_group,
                    "website"      : link,
                    "source"       : result["source"],
                    "snippet"      : result.get("snippet", ""),
                    "phone"        : "",
                    "email"        : "",
                    "address"      : "",
                    "description"  : "",
                    "scraped_at"   : datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                if self.scrape_details and link.startswith("http"):
                    details = self._scrape_detail(link)
                    entry.update({k: details.get(k, "") for k in ("phone", "email", "address", "description")})
                    time.sleep(random.uniform(1, 2))

                city_results.append(entry)

            time.sleep(random.uniform(2, 5))   # Arama motorunu yormamak için

        return city_results

    # ------------------------------------------------------------------
    def run(self, max_cities: int = None) -> pd.DataFrame:
        cities = self.cities[:max_cities] if max_cities else self.cities

        logger.info(f"\n{'='*60}")
        logger.info(f"  Nijerya Firma Bulucu — BAŞLADI")
        logger.info(f"  Ürün  : {self.product_group}")
        logger.info(f"  Şehir : {len(cities)}")
        logger.info(f"{'='*60}\n")

        for city_info in tqdm(cities, desc="Şehirler taranıyor"):
            logger.info(f"📍 {city_info['city']} ({city_info['region']}) ...")
            results = self._search_city(city_info)
            self.results.extend(results)
            logger.info(f"   ✅ {len(results)} firma")
            time.sleep(random.uniform(3, 6))

        df = pd.DataFrame(self.results)
        logger.info(f"\n🎉 Toplam {len(df)} firma kaydı toplandı!")
        return df

    # ------------------------------------------------------------------
    def save_results(self, df: pd.DataFrame, output_dir: str = "output"):
        """CSV + Excel (bölge bazlı sayfalar) + özet TXT kaydet"""
        os.makedirs(output_dir, exist_ok=True)
        ts   = datetime.now().strftime("%Y%m%d_%H%M%S")
        slug = self.product_group.replace(" ", "_").lower()

        # CSV
        csv_path = os.path.join(output_dir, f"nigeria_{slug}_{ts}.csv")
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")

        # Excel
        xlsx_path = os.path.join(output_dir, f"nigeria_{slug}_{ts}.xlsx")
        with pd.ExcelWriter(xlsx_path, engine="openpyxl") as writer:
            df.to_excel(writer, sheet_name="All Results", index=False)
            for region in df["region"].unique() if not df.empty else []:
                df[df["region"] == region].to_excel(
                    writer, sheet_name=region[:31], index=False
                )

        # Özet TXT
        summary_path = os.path.join(output_dir, f"summary_{slug}_{ts}.txt")
        with open(summary_path, "w", encoding="utf-8") as f:
            f.write("NIJERYA FİRMA BULUCU — ÖZET RAPOR\n")
            f.write("="*50 + "\n")
            f.write(f"Ürün Grubu : {self.product_group}\n")
            f.write(f"Tarih      : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Toplam Firm: {len(df)}\n\n")

            if not df.empty:
                f.write("BÖLGE BAZLI DAĞILIM:\n" + "-"*40 + "\n")
                for (region, city), grp in df.groupby(["region", "city"]):
                    f.write(f"  {region} > {city}: {len(grp)} firma\n")

                f.write("\nKAYNAK DAĞILIMI:\n" + "-"*40 + "\n")
                for src, cnt in df["source"].value_counts().items():
                    f.write(f"  {src}: {cnt}\n")

        logger.info(f"📄 CSV    : {csv_path}")
        logger.info(f"📊 Excel  : {xlsx_path}")
        logger.info(f"📝 Özet   : {summary_path}")

        return csv_path, xlsx_path, summary_path
