"""
Google (SerpAPI), Bing, DuckDuckGo tabanlı firma veri toplayıcı
Sandbox/server ortamlarında direkt scraping engeli olabilir.
SerpAPI veya Bing Search API kullanımı önerilir.
"""

import requests
import time
import random
import re
import logging
import os
from bs4 import BeautifulSoup
from urllib.parse import quote_plus

logger = logging.getLogger(__name__)

# =============================================
# API Anahtarları (.env veya environment'tan)
# =============================================
SERPAPI_KEY     = os.getenv("SERPAPI_KEY", "")       # https://serpapi.com (ücretsiz: 100/ay)
BING_API_KEY    = os.getenv("BING_API_KEY", "")      # Azure ücretsiz katman
SCRAPERAPI_KEY  = os.getenv("SCRAPERAPI_KEY", "")    # https://scraperapi.com


HEADERS_LIST = [
    {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122.0.0.0 Safari/537.36",
     "Accept-Language": "en-US,en;q=0.5"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15",
     "Accept-Language": "en-GB,en;q=0.9"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0",
     "Accept-Language": "en-US,en;q=0.5"},
]

def get_headers():
    return random.choice(HEADERS_LIST)


# =============================================
# 1. SerpAPI (Google) - ÖNERİLEN
# =============================================
def search_serpapi(query: str, num_results: int = 10) -> list:
    """SerpAPI üzerinden Google arama (en güvenilir yöntem)"""
    if not SERPAPI_KEY:
        logger.debug("SERPAPI_KEY bulunamadı, atlanıyor.")
        return []
    
    results = []
    try:
        params = {
            "q": query,
            "api_key": SERPAPI_KEY,
            "num": num_results,
            "gl": "ng",          # Nigeria
            "hl": "en",
        }
        r = requests.get("https://serpapi.com/search", params=params, timeout=20)
        data = r.json()
        
        for item in data.get("organic_results", [])[:num_results]:
            results.append({
                "source": "Google (SerpAPI)",
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "snippet": item.get("snippet", "")[:300]
            })
        logger.info(f"SerpAPI: {len(results)} sonuç")
    except Exception as e:
        logger.error(f"SerpAPI hata: {e}")
    
    return results


# =============================================
# 2. Bing Web Search API - ÜCRETSİZ DENEME
# =============================================
def search_bing_api(query: str, num_results: int = 10) -> list:
    """Bing Search API (Azure ücretsiz katman: 1000 sorgu/ay)"""
    if not BING_API_KEY:
        logger.debug("BING_API_KEY bulunamadı, atlanıyor.")
        return []
    
    results = []
    try:
        headers = {"Ocp-Apim-Subscription-Key": BING_API_KEY}
        params = {
            "q": query,
            "count": num_results,
            "mkt": "en-NG",
            "safeSearch": "Off"
        }
        r = requests.get(
            "https://api.bing.microsoft.com/v7.0/search",
            headers=headers, params=params, timeout=20
        )
        data = r.json()
        
        for item in data.get("webPages", {}).get("value", [])[:num_results]:
            results.append({
                "source": "Bing API",
                "title": item.get("name", ""),
                "link": item.get("url", ""),
                "snippet": item.get("snippet", "")[:300]
            })
        logger.info(f"Bing API: {len(results)} sonuç")
    except Exception as e:
        logger.error(f"Bing API hata: {e}")
    
    return results


# =============================================
# 3. ScraperAPI üzerinden Google HTML
# =============================================
def search_google_via_scraperapi(query: str, num_results: int = 10) -> list:
    """ScraperAPI proxy üzerinden Google HTML scraping"""
    if not SCRAPERAPI_KEY:
        logger.debug("SCRAPERAPI_KEY bulunamadı, atlanıyor.")
        return []
    
    results = []
    try:
        google_url = f"https://www.google.com/search?q={quote_plus(query)}&num={num_results}&gl=ng"
        api_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={quote_plus(google_url)}&country_code=ng"
        
        r = requests.get(api_url, timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for div in soup.find_all(['div'], class_=['g', 'tF2Cxc'])[:num_results]:
            title_tag = div.find(['h3', 'h2'])
            title = title_tag.get_text(strip=True) if title_tag else ""
            
            a_tag = div.find('a', href=True)
            link = ""
            if a_tag:
                href = a_tag['href']
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                elif href.startswith('http') and 'google' not in href:
                    link = href
            
            snippet_tag = div.find(['span', 'div'], class_=['VwiC3b', 'aCOpRe'])
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else ""
            
            if title and link:
                results.append({
                    "source": "Google (ScraperAPI)",
                    "title": title,
                    "link": link,
                    "snippet": snippet[:300]
                })
        logger.info(f"ScraperAPI/Google: {len(results)} sonuç")
    except Exception as e:
        logger.error(f"ScraperAPI hata: {e}")
    
    return results


# =============================================
# 4. Direkt HTML Scraping (proxy olmadan)
# =============================================
def search_google_direct(query: str, num_results: int = 10) -> list:
    """Direkt Google scraping (IP engellemeleri olabilir - proxy önerin)"""
    results = []
    try:
        encoded = quote_plus(query)
        url = f"https://www.google.com/search?q={encoded}&num={num_results}&hl=en&gl=ng"
        
        r = requests.get(url, headers=get_headers(), timeout=15)
        if r.status_code != 200:
            logger.warning(f"Google direkt: HTTP {r.status_code}")
            return results
        
        soup = BeautifulSoup(r.text, 'html.parser')
        
        for div in soup.find_all('div', class_=['g', 'tF2Cxc', 'MjjYud'])[:num_results]:
            title_tag = div.find(['h3', 'h2'])
            title = title_tag.get_text(strip=True) if title_tag else ""
            
            a_tag = div.find('a', href=True)
            link = ""
            if a_tag:
                href = a_tag.get('href', '')
                if href.startswith('/url?q='):
                    link = href.split('/url?q=')[1].split('&')[0]
                elif href.startswith('http') and 'google' not in href:
                    link = href
            
            snippet_tag = div.find(['span', 'div'], class_=['VwiC3b', 'aCOpRe'])
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else div.get_text(strip=True)[:200]
            
            if title and link:
                results.append({
                    "source": "Google (Direct)",
                    "title": title,
                    "link": link,
                    "snippet": snippet[:300]
                })
        logger.info(f"Google direkt: {len(results)} sonuç")
    except Exception as e:
        logger.error(f"Google direkt hata: {e}")
    
    return results


def search_yandex(query: str, num_results: int = 10) -> list:
    """Yandex HTML scraping"""
    results = []
    try:
        encoded = quote_plus(query)
        url = f"https://yandex.com/search/?text={encoded}&lang=en"
        r = requests.get(url, headers=get_headers(), timeout=15)
        
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.find_all(['li', 'div'], class_=re.compile(r'serp-item|organic'))
        
        for item in items[:num_results]:
            title_tag = item.find(['h2', 'h3', 'a'], class_=re.compile(r'title|organic__title'))
            title = title_tag.get_text(strip=True) if title_tag else ""
            
            link_tag = item.find('a', href=True)
            link = ""
            if link_tag:
                href = link_tag['href']
                if href.startswith('http') and 'yandex' not in href:
                    link = href
            
            snippet_tag = item.find(['p', 'span', 'div'], class_=re.compile(r'snippet|text'))
            snippet = snippet_tag.get_text(strip=True) if snippet_tag else item.get_text(strip=True)[:200]
            
            if title and link:
                results.append({
                    "source": "Yandex",
                    "title": title,
                    "link": link,
                    "snippet": snippet[:300]
                })
        logger.info(f"Yandex: {len(results)} sonuç")
    except Exception as e:
        logger.error(f"Yandex hata: {e}")
    
    return results


# =============================================
# ANA ARAMA FONKSİYONU - tüm kaynakları dener
# =============================================
def search_all(query: str, num_results: int = 10) -> list:
    """
    Mevcut API anahtarlarına göre en iyi kaynağı kullan.
    Öncelik: SerpAPI > Bing API > ScraperAPI > Direkt
    """
    results = []
    
    # 1. SerpAPI (en güvenilir)
    if SERPAPI_KEY:
        results = search_serpapi(query, num_results)
        if results:
            return results
    
    # 2. Bing API
    if BING_API_KEY:
        results = search_bing_api(query, num_results)
        if results:
            return results
    
    # 3. ScraperAPI
    if SCRAPERAPI_KEY:
        results = search_google_via_scraperapi(query, num_results)
        if results:
            return results
    
    # 4. Direkt (son çare)
    results = search_google_direct(query, num_results)
    time.sleep(random.uniform(2, 4))
    
    # 5. Yandex
    yandex_results = search_yandex(query, num_results // 2)
    results.extend(yandex_results)
    
    return results


# =============================================
# İletişim Bilgisi Çıkartıcı
# =============================================
def extract_contact_info(text: str) -> dict:
    phones = re.findall(
        r'(?:\+?234|0)[\s\-]?[789][01]\d[\s\-]?\d{3}[\s\-]?\d{4}',
        text
    )
    emails = re.findall(r'[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', text)
    websites = re.findall(r'https?://(?:www\.)?[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:/[^\s]*)?', text)
    return {
        "phones": list(set(phones))[:3],
        "emails": list(set(emails))[:3],
        "websites": list(set(websites))[:3]
    }


def scrape_company_details(url: str, timeout: int = 10) -> dict:
    """Firma web sitesinden iletişim bilgilerini çek"""
    details = {"address": "", "phone": "", "email": "", "description": ""}
    try:
        # ScraperAPI proxy kullan (varsa)
        if SCRAPERAPI_KEY:
            fetch_url = f"http://api.scraperapi.com/?api_key={SCRAPERAPI_KEY}&url={quote_plus(url)}"
        else:
            fetch_url = url
        
        r = requests.get(fetch_url, headers=get_headers(), timeout=timeout)
        if r.status_code != 200:
            return details
        
        soup = BeautifulSoup(r.text, 'html.parser')
        text = soup.get_text(separator=' ', strip=True)
        
        contact = extract_contact_info(text)
        
        # Adres
        for pattern in [
            r'\d+[,\s]+[A-Za-z\s]+(?:Street|Road|Avenue|Lane|Close|Drive|Way|Crescent)[,\s]+[A-Za-z\s,]+Nigeria',
        ]:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                details["address"] = match.group(0)[:200]
                break
        
        if contact["phones"]:
            details["phone"] = contact["phones"][0]
        if contact["emails"]:
            details["email"] = contact["emails"][0]
        
        meta_desc = soup.find('meta', attrs={'name': 'description'})
        if meta_desc and meta_desc.get('content'):
            details["description"] = meta_desc['content'][:300]
        
    except Exception as e:
        logger.debug(f"Detay hata ({url}): {e}")
    
    return details
