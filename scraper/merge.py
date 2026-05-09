"""
MGOSANI — Dataset Merger
Combines all scraped JSONL files into one final dataset.
Deduplicates and filters short texts.
"""

import json
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "mgosani_dataset.jsonl"

SOURCES = [
    "wikipedia.jsonl",
    "news.jsonl",
    "common_crawl.jsonl",
]

MIN_LENGTH = 100  # minimum characters


def merge():
    seen = set()
    total = 0
    skipped = 0

    with open(OUTPUT_FILE, "w", encoding="utf-8") as out:
        for source_file in SOURCES:
            path = DATA_DIR / source_file
            if not path.exists():
                print(f"  Skipping {source_file} (not found)")
                continue

            count = 0
            with open(path, encoding="utf-8") as f:
                for line in f:
                    try:
                        record = json.loads(line)
                        text = record.get("text", "").strip()

                        if len(text) < MIN_LENGTH:
                            skipped += 1
                            continue

                        # deduplicate by hash
                        h = hashlib.md5(text.encode()).hexdigest()
                        if h in seen:
                            skipped += 1
                            continue
                        seen.add(h)

                        out.write(json.dumps({"text": text}, ensure_ascii=False) + "\n")
                        count += 1
                        total += 1
                    except Exception:
                        continue

            print(f"  {source_file}: {count} records")

    print(f"\nFinal dataset: {total} records ({skipped} skipped)")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge()
