"""
MGOSANI — Georgian News Scraper
Scrapes articles from Georgian news sites and saves as JSONL.
"""

import json
import time
import requests
from bs4 import BeautifulSoup
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "news.jsonl"

SOURCES = [
    {
        "name": "civil.ge",
        "sitemap": "https://civil.ge/sitemap.xml",
        "article_selector": "div.entry-content",
        "lang": "ka",
    },
    {
        "name": "netgazeti.ge",
        "sitemap": "https://netgazeti.ge/sitemap.xml",
        "article_selector": "div.entry-content",
        "lang": "ka",
    },
    {
        "name": "interpressnews.ge",
        "sitemap": "https://www.interpressnews.ge/sitemap.xml",
        "article_selector": "div.article-body",
        "lang": "ka",
    },
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; MGOSANIbot/1.0; +https://github.com/Pistolmani/mgosani)"
}


def get_urls_from_sitemap(sitemap_url, limit=500):
    """Extract article URLs from a sitemap."""
    try:
        response = requests.get(sitemap_url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "xml")
        urls = [loc.text for loc in soup.find_all("loc") if loc.text.endswith("/") is False]
        return urls[:limit]
    except Exception as e:
        print(f"  Sitemap error for {sitemap_url}: {e}")
        return []


def scrape_article(url, selector):
    """Scrape article text from a URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.select_one(selector)
        if not content:
            return None
        text = content.get_text(separator="\n").strip()
        return text if len(text) > 150 else None
    except Exception as e:
        return None


def scrape(max_per_source=500):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    total = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for source in SOURCES:
            print(f"\nScraping {source['name']}...")
            urls = get_urls_from_sitemap(source["sitemap"], limit=max_per_source)
            print(f"  Found {len(urls)} URLs")
            count = 0

            for i, url in enumerate(urls):
                text = scrape_article(url, source["article_selector"])
                if text:
                    record = {
                        "text": text,
                        "source": source["name"],
                        "url": url,
                    }
                    f.write(json.dumps(record, ensure_ascii=False) + "\n")
                    count += 1

                if i % 50 == 0:
                    print(f"  [{i}/{len(urls)}] {count} articles saved")

                time.sleep(0.3)  # be polite

            print(f"  {source['name']}: {count} articles saved")
            total += count

    print(f"\nDone. {total} total news articles saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape()
