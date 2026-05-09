"""
MGOSANI — Common Crawl Georgian Data Fetcher
Downloads pre-filtered Georgian text from Hugging Face (CC-100 dataset).
No GPU needed — runs on CPU. Free.
"""

import json
from pathlib import Path

OUTPUT_FILE = Path(__file__).parent.parent / "data" / "common_crawl.jsonl"


def fetch():
    try:
        from datasets import load_dataset
    except ImportError:
        print("Installing datasets library...")
        import subprocess
        subprocess.run(["pip", "install", "datasets"], check=True)
        from datasets import load_dataset

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    print("Downloading Georgian CC-100 dataset from Hugging Face...")
    print("(This may take a few minutes — it's ~500MB)")

    dataset = load_dataset(
        "cc100",
        lang="ka",
        split="train",
        streaming=True,  # stream so we don't need to download all at once
        trust_remote_code=True,
    )

    count = 0
    max_records = 200_000  # 200k sentences is plenty

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for record in dataset:
            text = record.get("text", "").strip()
            if len(text) < 50:
                continue
            f.write(json.dumps({"text": text, "source": "cc100"}, ensure_ascii=False) + "\n")
            count += 1

            if count % 10_000 == 0:
                print(f"  {count} records saved...")

            if count >= max_records:
                break

    print(f"Done. {count} records saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    fetch()
