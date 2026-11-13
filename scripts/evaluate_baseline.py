"""
scripts/evaluate_baseline.py
Run the frozen LLM baseline evaluation across all 30 topics.
Author: Ankush Gupta (MRA2026003)

Usage:
    python scripts/evaluate_baseline.py --config configs/experiment_blueprint.yaml
"""

import argparse
import json
import yaml
import csv
from pathlib import Path
from datetime import datetime

from src.generator import load_model, generate_literature_review
from src.evaluator import compute_car


def main(config_path: str):
    with open(config_path) as f:
        config = yaml.safe_load(f)

    # Load model
    print("Loading model...")
    model, tokenizer = load_model(
        model_name=config["model"]["name"],
        quantize=(config["model"]["quantization"] == "4bit"),
    )

    # Load topics
    topics_path = "configs/topics.yaml"
    with open(topics_path) as f:
        topics_cfg = yaml.safe_load(f)

    all_topics = []
    for bin_name, topic_list in topics_cfg["topics"].items():
        for topic in topic_list:
            all_topics.append({"topic": topic, "bin": bin_name})

    results = []
    output_dir = Path("results")
    output_dir.mkdir(exist_ok=True)

    for item in all_topics:
        topic = item["topic"]
        bin_name = item["bin"]
        print(f"[{bin_name}] Evaluating: {topic}")

        # Generate review (baseline — no RAG)
        review = generate_literature_review(
            topic=topic,
            model=model,
            tokenizer=tokenizer,
            temperature=config["model"]["temperature"],
            max_new_tokens=config["model"]["max_new_tokens"],
            seed=config["model"]["seed"],
        )

        # Evaluate
        car, citation_statuses = compute_car(review)

        result = {
            "topic": topic,
            "bin": bin_name,
            "condition": "baseline",
            "car": car,
            "review": review,
            "citation_statuses": citation_statuses,
            "timestamp": datetime.now().isoformat(),
        }
        results.append(result)
        print(f"  CAR: {car:.3f}")

        # Save incrementally
        with open(output_dir / "baseline_results.jsonl", "a") as f:
            f.write(json.dumps(result) + "\n")

    # Write summary CSV
    with open(output_dir / "baseline_summary.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["topic", "bin", "condition", "car"])
        writer.writeheader()
        for r in results:
            writer.writerow({k: r[k] for k in ["topic", "bin", "condition", "car"]})

    print(f"\nDone. Results saved to {output_dir}/")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/experiment_blueprint.yaml")
    args = parser.parse_args()
    main(args.config)
