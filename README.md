# 🇳🇬 Nigeria Business Finder

Nijerya'daki firmaları **ürün grubuna** ve **bölgeye** göre otomatik olarak  
Google, Yandex ve Bing üzerinden bulan Python ajanı.

---

## 📋 İçindekiler

- [Özellikler](#-özellikler)
- [Gereksinimler](#-gereksinimler)
- [Kurulum](#-kurulum)
- [API Anahtarı Alma](#-api-anahtarı-alma-ücretsiz)
- [Kullanım](#-kullanım)
- [Bölgeler](#-nijerya-bölgeleri)
- [Çıktı Formatı](#-çıktı-formatı)
- [Mimari](#-mimari)
- [Sık Karşılaşılan Sorunlar](#-sık-karşılaşılan-sorunlar)

---

## ✨ Özellikler

- 🗺️ Nijerya'yı **6 bölge / 37 şehir** olarak otomatik böler
- 🔍 **Google, Yandex, Bing** üzerinden eş zamanlı arama yapar
- 📞 Her firma için **telefon, e-posta, adres, website** toplar
- 📊 Sonuçları **CSV + Excel (bölge bazlı sayfalar)** olarak kaydeder
- ⚡ Hem hızlı mod (`--no-scrape`) hem de derin tarama desteği
- 🔑 **SerpAPI / Bing API / ScraperAPI** entegrasyonu (ücretsiz katmanlar)

---

## 🖥️ Gereksinimler

| Gereksinim | Versiyon |
|------------|----------|
| Python     | 3.9+     |
| pip        | 21+      |
| İnternet   | ✅       |

> Windows, macOS ve Linux üzerinde çalışır.

---

## 🚀 Kurulum

### 1. Repoyu Klonla

```bash
git clone https://github.com/KULLANICI_ADIN/nigeria-business-finder.git
cd nigeria-business-finder
```

> **ZIP ile indirdiyseniz:**
> ```bash
> unzip nigeria-business-finder.zip
> cd nigeria-business-finder
> ```

---

### 2. Sanal Ortam Oluştur (Önerilir)

```bash
# Sanal ortam oluştur
python -m venv venv

# Aktive et — Windows
venv\Scripts\activate

# Aktive et — macOS / Linux
source venv/bin/activate
```

---

### 3. Bağımlılıkları Yükle

```bash
pip install -r requirements.txt
```

Yüklenen paketler:

| Paket | Amaç |
|-------|------|
| `requests` | HTTP istekleri |
| `beautifulsoup4` + `lxml` | HTML parsing |
| `pandas` | Veri işleme |
| `openpyxl` | Excel çıktısı |
| `tqdm` | İlerleme çubuğu |
| `fake-useragent` | Bot tespitini azaltma |

---

### 4. API Anahtarlarını Ayarla

```bash
# Şablon dosyayı kopyala
cp .env.example .env

# Dosyayı aç ve anahtarları gir
nano .env        # Linux / macOS
notepad .env     # Windows
```

`.env` dosyası içeriği:

```env
SERPAPI_KEY=buraya_kendi_anahtarini_yaz
BING_API_KEY=buraya_kendi_anahtarini_yaz
SCRAPERAPI_KEY=buraya_kendi_anahtarini_yaz
```

> En az **bir** anahtar girilmesi yeterlidir.  
> Hiç girilmezse sistem direkt scraping yapar (bot engeliyle karşılaşabilirsiniz).

---

## 🔑 API Anahtarı Alma (Ücretsiz)

### SerpAPI — 100 ücretsiz sorgu/ay ✅ Önerilen

1. [serpapi.com](https://serpapi.com) adresine git
2. **"Sign Up Free"** butonuna tıkla
3. E-posta ile kayıt ol
4. Dashboard → **API Key** bölümünden anahtarı kopyala
5. `.env` dosyasına `SERPAPI_KEY=...` olarak yapıştır

---

### Bing Search API — 1.000 ücretsiz sorgu/ay

1. [portal.azure.com](https://portal.azure.com) adresine git
2. Ücretsiz hesap oluştur (kredi kartı gerekebilir, ücret yok)
3. Arama çubuğunda **"Bing Search v7"** ara
4. **Create** → Ücretsiz katman (F0) seç
5. Kaynak oluştuktan sonra → **Keys and Endpoint** → Key1'i kopyala
6. `.env` dosyasına `BING_API_KEY=...` olarak yapıştır

---

### ScraperAPI — 1.000 ücretsiz istek/ay

1. [scraperapi.com](https://scraperapi.com) adresine git
2. **"Start Free Trial"** butonuna tıkla
3. Kayıt ol → Dashboard → API Key'i kopyala
4. `.env` dosyasına `SCRAPERAPI_KEY=...` olarak yapıştır

---

## 💻 Kullanım

### Temel Komutlar

```bash
# Tüm Nijerya'da güneş paneli firmaları ara
python main.py --product "solar panels"

# Sadece Güneybatı bölgesinde çimento firmaları
python main.py --product "cement" --regions "South West"

# Birden fazla bölge
python main.py --product "rice distribution" --regions "North West" "North East" "North Central"

# Bölgeleri listele
python main.py --list-regions
```

### Hız ve Kapsam Seçenekleri

```bash
# Hızlı mod — firma sitelerini ziyaret etme (sadece arama sonuçları)
python main.py --product "agricultural equipment" --no-scrape

# Test — sadece 5 şehir tara
python main.py --product "solar panels" --max-cities 5

# Özel çıktı klasörü
python main.py --product "cement" --output-dir sonuclar/
```

### Python API Olarak Kullan

```python
from src.finder import NigeriaBusinessFinder

finder = NigeriaBusinessFinder(
    product_group="solar panels",      # Aranacak ürün
    regions=["South West", "North West"],  # None = tüm Nijerya
    scrape_details=True                # Firma sitelerini de tara
)

df = finder.run(max_cities=10)         # max_cities=None = tümü
finder.save_results(df, output_dir="sonuclar")

print(df[["company_name", "city", "phone", "email"]].head(10))
```

---

## 🗺️ Nijerya Bölgeleri

| Bölge | Büyük Şehirler |
|-------|----------------|
| **North West** | Kano, Kaduna, Katsina, Sokoto, Birnin Kebbi, Gusau, Dutse |
| **North East** | Maiduguri, Yola, Bauchi, Gombe, Jalingo, Damaturu |
| **North Central** | Abuja, Minna, Makurdi, Lokoja, Ilorin, Lafia, Jos |
| **South West** | Lagos, Ibadan, Abeokuta, Osogbo, Akure, Ado-Ekiti |
| **South East** | Onitsha, Owerri, Enugu, Abakaliki, Umuahia |
| **South South** | Port Harcourt, Warri, Calabar, Uyo, Benin City, Yenagoa |

---

## 📂 Çıktı Formatı

```
output/
├── nigeria_solar_panels_20240315_143022.csv     ← Tüm veriler (UTF-8)
├── nigeria_solar_panels_20240315_143022.xlsx    ← Bölge bazlı sayfalar
└── summary_solar_panels_20240315_143022.txt     ← Özet rapor
```

### CSV / Excel Sütunları

| Sütun | Açıklama |
|-------|----------|
| `company_name` | Firma adı |
| `city` | Şehir |
| `region` | Nijerya bölgesi |
| `product_group` | Aranan ürün grubu |
| `website` | Firma websitesi |
| `source` | Kaynak (Google / Yandex / Bing) |
| `phone` | Telefon numarası |
| `email` | E-posta adresi |
| `address` | Adres |
| `description` | Firma açıklaması |
| `snippet` | Arama sonucu özeti |
| `scraped_at` | Tarama tarihi/saati |

---

## 🏗️ Mimari

```
nigeria-business-finder/
├── main.py                    ← CLI giriş noktası
├── requirements.txt           ← Python bağımlılıkları
├── .env.example               ← API key şablonu
├── src/
│   ├── scraper.py            ← Google/Yandex/Bing arayıcı + iletişim çıkartıcı
│   └── finder.py             ← NigeriaBusinessFinder sınıfı (ana iş mantığı)
├── data/
│   └── nigeria_regions.py    ← 6 bölge / 37 şehir veritabanı
└── output/                   ← Sonuçlar burada oluşur
```

---

## ❓ Sık Karşılaşılan Sorunlar

### `ModuleNotFoundError: No module named 'xxx'`
```bash
pip install -r requirements.txt
```

### `0 sonuç bulundu` — API anahtarı yok
`.env` dosyasına en az bir API anahtarı ekleyin (bkz. [API Anahtarı Alma](#-api-anahtarı-alma-ücretsiz))

### Google / Yandex bot engeli
SerpAPI veya ScraperAPI kullanın — direkt scraping sandbox/bulut ortamlarında engellenir.

### `.env dosyası okunmuyor`
```bash
pip install python-dotenv
```
ve `main.py` başına şunu ekleyin:
```python
from dotenv import load_dotenv
load_dotenv()
```

### Windows'ta `activate` komutu çalışmıyor
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
venv\Scripts\activate
```

---

## 📄 Lisans

MIT License — dilediğiniz gibi kullanabilir, değiştirebilir ve dağıtabilirsiniz.
