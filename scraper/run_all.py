"""
MGOSANI — Run All Scrapers
Run this to collect all Georgian data in one go.
"""

import wikipedia
import news
import common_crawl
import merge

print("=" * 50)
print("MGOSANI Data Collection Pipeline")
print("=" * 50)

print("\n[1/4] Wikipedia...")
wikipedia.scrape()

print("\n[2/4] News sites...")
news.scrape()

print("\n[3/4] Common Crawl (CC-100)...")
common_crawl.fetch()

print("\n[4/4] Merging all sources...")
merge.merge()

print("\nAll done! Your dataset is at data/mgosani_dataset.jsonl")
print("Upload it to Hugging Face and fine-tune on Kaggle.")
