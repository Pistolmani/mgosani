"""
MGOSANI — Dataset Merger
Combines all scraped JSONL files into one final dataset.
Deduplicates and filters short texts. Preserves source and license metadata.
"""

import json
import hashlib
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
OUTPUT_FILE = DATA_DIR / "raw_georgian.jsonl"

# news.jsonl excluded — civil.ge/netgazeti ToS prohibits ML training use
SOURCES = [
    "wikipedia.jsonl",
    "common_crawl.jsonl",
]

LICENSE_MAP = {
    "wikipedia": "CC BY-SA 4.0",
    "cc100": "Common Crawl Terms of Use",
}

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

                        h = hashlib.md5(text.encode()).hexdigest()
                        if h in seen:
                            skipped += 1
                            continue
                        seen.add(h)

                        source = record.get("source", source_file.replace(".jsonl", ""))
                        out_record = {
                            "text": text,
                            "source": source,
                            "license": LICENSE_MAP.get(source, "unknown"),
                        }
                        out.write(json.dumps(out_record, ensure_ascii=False) + "\n")
                        count += 1
                        total += 1
                    except Exception:
                        continue

            print(f"  {source_file}: {count} records")

    print(f"\nFinal dataset: {total} records ({skipped} skipped)")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    merge()
