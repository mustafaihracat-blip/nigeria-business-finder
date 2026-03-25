import argparse
import logging
import sys
import os
import pandas as pd

# ── 1. Proje kök dizinini Python path'e ekle ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── 2. .env dosyasını yükle (varsa) ──────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  

# ── 3. output/ klasörünü oluştur ──────────────
os.makedirs("output", exist_ok=True)

# ── 4. Logging ayarla ─────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(os.path.join("output", "finder.log"), mode="a", encoding="utf-8"),
    ],
)

# ── 5. Modülleri import et ────────────────────────────────────────────────────
from src.finder import NigeriaBusinessFinder
from data.nigeria_regions import NIGERIA_REGIONS

# --- ARAYÜZ İÇİN GEREKLİ FONKSİYON (Streamlit burayı çağıracak) ---
def find_nigeria_businesses(product, max_cities=2):
    """Streamlit arayüzü için basitleştirilmiş çalıştırma fonksiyonu"""
    finder = NigeriaBusinessFinder(
        product_group=product,
        regions=None, # Tüm bölgeler
        scrape_details=True,
    )
    df = finder.run(max_cities=max_cities)
    
    if not df.empty:
        csv_path, xlsx_path, summary_path = finder.save_results(df, output_dir="output")
        return df, xlsx_path
    return pd.DataFrame(), None

# ── 6. Ana Terminal Girişi ───────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="🇳🇬 Nijerya Firma Bulucu")
    parser.add_argument("--product", "-p", type=str, help="Aranacak ürün")
    parser.add_argument("--regions", "-r", nargs="+", type=str, choices=list(NIGERIA_REGIONS.keys()))
    parser.add_argument("--max-cities", "-m", type=int, default=None)
    parser.add_argument("--no-scrape", action="store_true")
    
    args = parser.parse_args()

    if not args.product:
        parser.print_help()
        sys.exit(1)

    finder = NigeriaBusinessFinder(
        product_group=args.product,
        regions=args.regions,
        scrape_details=not args.no_scrape,
    )

    df = finder.run(max_cities=args.max_cities)

    if df.empty:
        logging.warning("Hiç sonuç bulunamadı.")
        return

    csv_path, xlsx_path, summary_path = finder.save_results(df, output_dir="output")
    logging.info(f"✅ İşlem Tamamlandı! Toplam: {len(df)} firma. Dosya: {xlsx_path}")

if __name__ == "__main__":
    main()
