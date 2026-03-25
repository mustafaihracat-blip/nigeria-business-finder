#!/usr/bin/env python3
"""
🇳🇬 Nijerya Firma Bulucu - Ana Giriş Noktası
==============================================
Kullanım:
    python main.py --product "solar panels"
    python main.py --product "cement distribution" --regions "South West" "North West"
    python main.py --product "rice" --max-cities 5 --no-scrape
"""

import argparse
import logging
import sys
import os

# ── 1. Proje kök dizinini Python path'e ekle ──────────────────────────────────
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── 2. .env dosyasını yükle (varsa) ──────────────────────────────────────────
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # python-dotenv kurulu değilse atla

# ── 3. output/ klasörünü ÖNCE oluştur (log dosyası için gerekli) ──────────────
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


# ─────────────────────────────────────────────────────────────────────────────
def list_regions():
    print("\n📍 Mevcut Nijerya Bölgeleri:")
    print("=" * 50)
    for region, data in NIGERIA_REGIONS.items():
        print(f"\n🗺️  {region}")
        print(f"   Eyaletler     : {', '.join(data['states'])}")
        print(f"   Büyük Şehirler: {', '.join(data['major_cities'])}")


# ─────────────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="🇳🇬 Nijerya Firma Bulucu — Google & Yandex & Bing tabanlı",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Örnekler:
  python main.py --product "solar panels"
  python main.py --product "cement" --regions "South West" "North West"
  python main.py --product "electrical equipment" --max-cities 2 --no-scrape
  python main.py --list-regions
        """,
    )

    parser.add_argument("--product",      "-p", type=str,
                        help="Aranacak ürün/sektör (ör: 'solar panels', 'cement')")
    parser.add_argument("--regions",      "-r", nargs="+", type=str,
                        choices=list(NIGERIA_REGIONS.keys()),
                        help="Sadece belirli bölgeler (boş bırakınca tüm Nijerya)")
    parser.add_argument("--max-cities",   "-m", type=int, default=None,
                        help="Maksimum şehir sayısı — test için (ör: 2)")
    parser.add_argument("--no-scrape",    action="store_true",
                        help="Firma web sitelerini ziyaret etme (hızlı mod)")
    parser.add_argument("--list-regions", action="store_true",
                        help="Mevcut bölgeleri listele ve çık")
    parser.add_argument("--output-dir",  "-o", type=str, default="output",
                        help="Çıktı klasörü (varsayılan: output)")

    args = parser.parse_args()

    # Sadece bölgeleri listele
    if args.list_regions:
        list_regions()
        return

    # --product zorunlu
    if not args.product:
        parser.print_help()
        print("\n❌ Hata: --product parametresi gerekli!")
        print("Örnek: python main.py --product 'solar panels'")
        sys.exit(1)

    # output-dir'i de baştan oluştur (varsayılan değil farklı bir yol verilmişse)
    os.makedirs(args.output_dir, exist_ok=True)

    # ── Finder'ı başlat ve çalıştır ──────────────────────────────────────────
    finder = NigeriaBusinessFinder(
        product_group=args.product,
        regions=args.regions,
        scrape_details=not args.no_scrape,
    )

    df = finder.run(max_cities=args.max_cities)

    if df.empty:
        print("\n⚠️  Hiç sonuç bulunamadı.")
        print("   • API anahtarınızı .env dosyasına eklediğinizden emin olun.")
        print("   • Ya da farklı bir ürün adı deneyin.")
        return

    csv_path, xlsx_path, summary_path = finder.save_results(df, output_dir=args.output_dir)

    print(f"\n{'='*60}")
    print(f"✅ TAMAMLANDI!")
    print(f"   Toplam Firma : {len(df)}")
    print(f"   CSV Dosyası  : {csv_path}")
    print(f"   Excel Dosyası: {xlsx_path}")
    print(f"   Özet Rapor   : {summary_path}")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
