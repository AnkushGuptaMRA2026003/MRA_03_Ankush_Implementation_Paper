"""
scripts/fetch_data.py
Pre-fetches and caches Semantic Scholar API responses for all 30 topics.
Run this once to avoid hitting rate limits during evaluation.
Author: Ankush Gupta (MRA2026003)

Usage:
    python scripts/fetch_data.py --config configs/experiment_blueprint.yaml
"""

import argparse
import json
import yaml
import time
from pathlib import Path

from src.rag_pipeline import retrieve_papers


def main(config_path: str):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    with open("configs/topics.yaml") as f:
        topics_cfg = yaml.safe_load(f)

    cache_dir = Path("data/cache")
    cache_dir.mkdir(parents=True, exist_ok=True)

    top_k = config["rag"]["top_k"]

    for bin_name, topic_list in topics_cfg["topics"].items():
        for topic in topic_list:
            safe_name = topic.replace(" ", "_").replace("/", "-")[:60]
            cache_file = cache_dir / f"{safe_name}.json"

            if cache_file.exists():
                print(f"  [CACHED] {topic}")
                continue

            print(f"  [FETCH]  {topic}")
            papers = retrieve_papers(topic, top_k=top_k)
            with open(cache_file, "w", encoding="utf-8") as f:
                json.dump({"topic": topic, "bin": bin_name, "papers": papers}, f, indent=2)

            time.sleep(1.0)  # Respect rate limits

    print(f"\nDone. {len(list(cache_dir.glob('*.json')))} topics cached in {cache_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiment_blueprint.yaml")
    args = parser.parse_args()
    main(args.config)
