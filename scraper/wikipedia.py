"""
MGOSANI — Georgian Wikipedia Scraper
Fetches all Georgian Wikipedia articles and saves them as JSONL.
"""

import json
import time
import requests
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "wikipedia.jsonl"
API_URL = "https://ka.wikipedia.org/w/api.php"

def get_all_page_titles():
    """Fetch all Georgian Wikipedia article titles."""
    titles = []
    params = {
        "action": "query",
        "list": "allpages",
        "aplimit": 500,
        "apnamespace": 0,
        "format": "json",
    }
    print("Fetching article titles...")
    while True:
        response = requests.get(API_URL, params=params).json()
        pages = response["query"]["allpages"]
        titles.extend(p["title"] for p in pages)
        print(f"  {len(titles)} titles so far...")

        if "continue" not in response:
            break
        params["apcontinue"] = response["continue"]["apcontinue"]
        time.sleep(0.2)

    print(f"Total titles: {len(titles)}")
    return titles


def get_article_text(title):
    """Fetch plain text of a Wikipedia article."""
    params = {
        "action": "query",
        "titles": title,
        "prop": "extracts",
        "explaintext": True,
        "exsectionformat": "plain",
        "format": "json",
    }
    response = requests.get(API_URL, params=params).json()
    pages = response["query"]["pages"]
    page = next(iter(pages.values()))
    return page.get("extract", "").strip()


def scrape(max_articles=None):
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    titles = get_all_page_titles()

    if max_articles:
        titles = titles[:max_articles]

    print(f"Scraping {len(titles)} articles...")
    count = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for i, title in enumerate(titles):
            try:
                text = get_article_text(title)
                if len(text) < 100:
                    continue  # skip stubs
                record = {"text": text, "source": "wikipedia", "title": title}
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
                count += 1
                if i % 100 == 0:
                    print(f"  [{i}/{len(titles)}] {count} articles saved")
                time.sleep(0.1)
            except Exception as e:
                print(f"  Error on '{title}': {e}")
                continue

    print(f"Done. {count} articles saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    scrape()
