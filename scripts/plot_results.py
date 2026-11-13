"""
scripts/plot_results.py
Generate figures from baseline and RAG evaluation results.
Author: Ankush Gupta (MRA2026003)

Usage:
    python scripts/plot_results.py --results_dir results/
"""

import argparse
import csv
import os
from pathlib import Path
from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import wilcoxon


def load_csv(path: str):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def main(results_dir: str):
    fig_dir = Path(results_dir) / "figures"
    fig_dir.mkdir(exist_ok=True)

    # Load results
    baseline = load_csv(os.path.join(results_dir, "baseline_summary.csv"))
    rag = load_csv(os.path.join(results_dir, "rag_summary.csv"))

    bins = ["pre_cutoff", "near_cutoff", "post_cutoff"]
    bin_labels = ["Pre-Cutoff\n(2020–2022)", "Near-Cutoff\n(2023)", "Post-Cutoff\n(2024–2025)"]

    # Compute mean CAR per bin per condition
    def group_by_bin(rows):
        grouped = defaultdict(list)
        for row in rows:
            grouped[row["bin"]].append(float(row["car"]))
        return grouped

    baseline_grouped = group_by_bin(baseline)
    rag_grouped = group_by_bin(rag)

    baseline_means = [np.mean(baseline_grouped[b]) for b in bins]
    rag_means = [np.mean(rag_grouped[b]) for b in bins]
    baseline_stds = [np.std(baseline_grouped[b]) for b in bins]
    rag_stds = [np.std(rag_grouped[b]) for b in bins]

    # --- Figure 1: Grouped bar chart ---
    x = np.arange(len(bins))
    width = 0.35

    fig, ax = plt.subplots(figsize=(8, 5))
    bars1 = ax.bar(x - width / 2, baseline_means, width, yerr=baseline_stds,
                   label="Frozen LLM Baseline", color="#4C72B0", capsize=4)
    bars2 = ax.bar(x + width / 2, rag_means, width, yerr=rag_stds,
                   label="LLM + RAG", color="#DD8452", capsize=4)

    ax.set_xlabel("Temporal Bin (relative to model knowledge cutoff)")
    ax.set_ylabel("Citation Accuracy Rate (CAR)")
    ax.set_title("Citation Accuracy Rate by Temporal Bin:\nFrozen LLM Baseline vs. RAG-Enhanced")
    ax.set_xticks(x)
    ax.set_xticklabels(bin_labels)
    ax.set_ylim(0, 1.0)
    ax.legend()
    ax.grid(axis="y", alpha=0.3)

    plt.tight_layout()
    plt.savefig(fig_dir / "car_barplot.png", dpi=150)
    print(f"Saved: {fig_dir}/car_barplot.png")
    plt.close()

    # --- Wilcoxon test on post-cutoff bin ---
    post_baseline = baseline_grouped["post_cutoff"]
    post_rag = rag_grouped["post_cutoff"]

    if len(post_baseline) >= 10 and len(post_rag) >= 10:
        stat, pval = wilcoxon(post_rag, post_baseline, alternative="greater")
        print(f"\nWilcoxon test (post-cutoff, RAG > Baseline): stat={stat:.3f}, p={pval:.4f}")

        with open(Path(results_dir) / "statistics.txt", "w") as f:
            f.write(f"Wilcoxon signed-rank test (post-cutoff bin, RAG > Baseline)\n")
            f.write(f"n = {len(post_baseline)}\n")
            f.write(f"Statistic = {stat:.3f}\n")
            f.write(f"p-value = {pval:.4f}\n")
            f.write(f"Significant (p < 0.05): {pval < 0.05}\n")

    # --- Figure 2: CAR degradation line plot ---
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(bin_labels, baseline_means, "o-", label="Frozen LLM Baseline", color="#4C72B0")
    ax.plot(bin_labels, rag_means, "s-", label="LLM + RAG", color="#DD8452")
    ax.fill_between(range(len(bins)),
                    [m - s for m, s in zip(baseline_means, baseline_stds)],
                    [m + s for m, s in zip(baseline_means, baseline_stds)],
                    alpha=0.15, color="#4C72B0")
    ax.fill_between(range(len(bins)),
                    [m - s for m, s in zip(rag_means, rag_stds)],
                    [m + s for m, s in zip(rag_means, rag_stds)],
                    alpha=0.15, color="#DD8452")
    ax.set_xticks(range(len(bins)))
    ax.set_xticklabels(bin_labels)
    ax.set_ylabel("Citation Accuracy Rate (CAR)")
    ax.set_title("CAR Degradation with Temporal Distance from Model Cutoff")
    ax.set_ylim(0, 1.0)
    ax.legend()
    ax.grid(alpha=0.3)

    plt.tight_layout()
    plt.savefig(fig_dir / "car_degradation.png", dpi=150)
    print(f"Saved: {fig_dir}/car_degradation.png")
    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--results_dir", default="results/")
    args = parser.parse_args()
    main(args.results_dir)
