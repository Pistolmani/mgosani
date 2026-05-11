"""
MGOSANI — Run All Scrapers
Run this to collect all Georgian data in one go.

NOTE: news.py (civil.ge, netgazeti.ge) is intentionally excluded —
their ToS prohibits ML training use. Use Wikipedia + CC-100 only.
"""

import wikipedia
import common_crawl
import merge

print("=" * 50)
print("MGOSANI Data Collection Pipeline")
print("=" * 50)

print("\n[1/3] Wikipedia...")
wikipedia.scrape()

print("\n[2/3] Common Crawl (CC-100)...")
common_crawl.fetch()

print("\n[3/3] Merging all sources...")
merge.merge()

print("\nAll done! Your dataset is at data/raw_georgian.jsonl")
