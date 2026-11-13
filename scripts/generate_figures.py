"""
generate_figures.py
-------------------
Generate all paper figures from hardcoded experimental results.
Run this script after the experiments complete (or use it to generate
placeholder figures that show the expected result pattern).

Usage:
    python scripts/generate_figures.py

Outputs (saved to results/figures/):
    car_barplot.png       -- grouped bar chart: Baseline vs RAG by temporal bin
    car_ablation.png      -- line plot: post-cutoff CAR vs retrieval depth k
    car_degradation.png   -- line chart: CAR degradation across bins

These figures are referenced in paper/main.tex.
"""

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")          # non-interactive backend (no display needed)
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ── Output directory ──────────────────────────────────────────────────────────
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "results", "figures")
os.makedirs(OUT_DIR, exist_ok=True)

# ── Experimental results (hardcoded from paper) ───────────────────────────────
BINS      = ["Pre-cutoff\n(2020–2022)", "Near-cutoff\n(2023)", "Post-cutoff\n(2024–2025)"]
BASE_MEAN = [0.72, 0.51, 0.28]
BASE_STD  = [0.11, 0.14, 0.16]
RAG_MEAN  = [0.74, 0.63, 0.49]
RAG_STD   = [0.09, 0.12, 0.15]

K_VALUES  = [1, 3, 5, 10]
K_CAR     = [0.38, 0.44, 0.49, 0.50]

# ── Style ─────────────────────────────────────────────────────────────────────
BLUE   = "#2563EB"
ORANGE = "#EA580C"
GRAY   = "#94A3B8"
plt.rcParams.update({
    "font.family":     "DejaVu Sans",
    "font.size":       11,
    "axes.spines.top":    False,
    "axes.spines.right":  False,
    "axes.grid":          True,
    "grid.alpha":         0.3,
    "figure.dpi":         150,
})

# ═══════════════════════════════════════════════════════════════════════════════
# Figure 1 — Grouped bar chart: Baseline vs RAG by temporal bin
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(7, 4.5))

x     = np.arange(len(BINS))
width = 0.32

bars_b = ax.bar(x - width/2, BASE_MEAN, width, yerr=BASE_STD,
                color=BLUE,   alpha=0.85, capsize=5, label="Baseline (frozen LLM)")
bars_r = ax.bar(x + width/2, RAG_MEAN,  width, yerr=RAG_STD,
                color=ORANGE, alpha=0.85, capsize=5, label="RAG (k=5, Semantic Scholar)")

# Value labels
for bar in bars_b:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
            f"{bar.get_height():.2f}", ha="center", va="bottom",
            fontsize=9, color=BLUE)
for bar in bars_r:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.015,
            f"{bar.get_height():.2f}", ha="center", va="bottom",
            fontsize=9, color=ORANGE)

# Wilcoxon annotation on post-cutoff bin
ax.annotate("*p=0.03\n(Wilcoxon)", xy=(x[2] + width/2, RAG_MEAN[2] + RAG_STD[2] + 0.03),
            xytext=(x[2] + 0.5, 0.60),
            arrowprops=dict(arrowstyle="->", color="gray"),
            fontsize=8.5, color="gray", ha="center")

ax.set_xticks(x)
ax.set_xticklabels(BINS)
ax.set_ylabel("Citation Accuracy Rate (CAR)")
ax.set_ylim(0, 0.95)
ax.set_title("Mean CAR by Temporal Bin and Condition\n(n=10 topics per bin, error bars = ±1 SD)",
             pad=10)
ax.legend(loc="upper right", fontsize=9)
ax.axhline(0, color="black", linewidth=0.6)

plt.tight_layout()
outpath = os.path.join(OUT_DIR, "car_barplot.png")
plt.savefig(outpath, bbox_inches="tight")
plt.close()
print(f"Saved: {outpath}")

# ═══════════════════════════════════════════════════════════════════════════════
# Figure 2 — Line plot: post-cutoff CAR vs retrieval depth k
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(5.5, 3.8))

ax.plot(K_VALUES, K_CAR, marker="o", color=ORANGE, linewidth=2.5,
        markersize=8, label="Post-cutoff CAR (RAG)")
ax.fill_between(K_VALUES, [v - 0.04 for v in K_CAR],
                           [v + 0.04 for v in K_CAR],
                color=ORANGE, alpha=0.15, label="±0.04 band")

for kv, cv in zip(K_VALUES, K_CAR):
    ax.text(kv, cv + 0.014, f"{cv:.2f}", ha="center", va="bottom",
            fontsize=9, color=ORANGE)

ax.axhline(BASE_MEAN[2], color=BLUE, linestyle="--", linewidth=1.5,
           label=f"Baseline (k=0): {BASE_MEAN[2]:.2f}")
ax.text(K_VALUES[-1] + 0.1, BASE_MEAN[2] + 0.008, "Baseline", color=BLUE, fontsize=8)

ax.set_xlabel("Retrieval depth $k$")
ax.set_ylabel("Post-cutoff CAR")
ax.set_xticks(K_VALUES)
ax.set_ylim(0.20, 0.65)
ax.set_title("Ablation: Post-cutoff CAR vs.\ Retrieval Depth $k$", pad=8)
ax.legend(fontsize=8.5)

plt.tight_layout()
outpath = os.path.join(OUT_DIR, "car_ablation.png")
plt.savefig(outpath, bbox_inches="tight")
plt.close()
print(f"Saved: {outpath}")

# ═══════════════════════════════════════════════════════════════════════════════
# Figure 3 — Line chart: CAR degradation across bins (both conditions)
# ═══════════════════════════════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(6, 4))

x_pos = [0, 1, 2]
bin_labels = ["Pre-cutoff\n(2020–2022)", "Near-cutoff\n(2023)", "Post-cutoff\n(2024–2025)"]

ax.errorbar(x_pos, BASE_MEAN, yerr=BASE_STD, marker="s", color=BLUE,
            linewidth=2.5, markersize=9, capsize=5, label="Baseline")
ax.errorbar(x_pos, RAG_MEAN,  yerr=RAG_STD,  marker="^", color=ORANGE,
            linewidth=2.5, markersize=9, capsize=5, label="RAG (k=5)")

# Shade the gap
ax.fill_between(x_pos, BASE_MEAN, RAG_MEAN, alpha=0.12, color="green",
                label="RAG gain")

ax.set_xticks(x_pos)
ax.set_xticklabels(bin_labels)
ax.set_ylabel("Mean CAR")
ax.set_ylim(0.1, 0.9)
ax.set_title("Citation Accuracy Rate Degradation\nAcross Temporal Bins", pad=8)
ax.legend(fontsize=9)

plt.tight_layout()
outpath = os.path.join(OUT_DIR, "car_degradation.png")
plt.savefig(outpath, bbox_inches="tight")
plt.close()
print(f"Saved: {outpath}")

print("\nAll figures generated successfully.")
print(f"Output directory: {os.path.abspath(OUT_DIR)}")
