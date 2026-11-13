# AITR Lab Assignment 02 — Knowledge Cutoff Effects on LLM-Generated Literature Reviews

**Student:** Ankush Gupta  
**Roll No.:** MRA2026003  
**Programme:** M.Tech. Information Technology (Robotics and AI)  
**Course:** AI Tools for Research — IIIT Allahabad  
**Assignment:** Lab 02 — From Review to Research  

---

## Research Question

> **How significantly does a large language model's knowledge cutoff degrade the quality of literature review generation in rapidly evolving AI subfields, and can retrieval-augmented generation (RAG) measurably close that gap?**

Sub-questions:
1. Can we quantify citation staleness and hallucination rates as a function of publication date relative to a model's cutoff?
2. Does RAG with a live academic index reduce hallucination rates compared to a frozen LLM baseline?
3. Which review quality metrics (citation accuracy, recency, claim coverage) are most sensitive to cutoff effects?

---

## Study Pathway

**Pathway A — Reproduction + Extension**  
Reproduce the controlled evaluation design from prior literature (Shaier et al., 2024; Walters & Wilder, 2023) using an open-source LLM, then extend the study by systematically varying the temporal gap between the model's effective cutoff and the query date.

---

## Repository Structure

```
AITR_Lab02_MRA2026003_LLMKnowledgeCutoff/
  README.md                 # This file — research question and reproducibility guide
  requirements.txt          # Verified Python dependencies
  configs/                  # Frozen experimental settings (YAML)
  data/README.md            # Dataset access instructions (no raw restricted data)
  notebooks/                # Exploration and verified runnable notebooks
  src/                      # Reusable functions and evaluation modules
  scripts/                  # Evaluation and pipeline entry-points
  results/                  # Genuine metric files, logs and figures
  paper/                    # LaTeX source, bibliography and figures
  research_decisions.md     # Literature-to-experiment decision log
  baseline_validation.md    # Reproduction checks and deviations
  ai_assistance_log.md      # Significant prompts and human verification steps
```

---

## Reproducibility

### Environment Setup

```bash
git clone <repo-url>
cd AITR_Lab02_MRA2026003_LLMKnowledgeCutoff
pip install -r requirements.txt
```

### Run Baseline Evaluation

```bash
python scripts/evaluate_baseline.py --config configs/baseline.yaml
```

### Run RAG-Enhanced Evaluation

```bash
python scripts/evaluate_rag.py --config configs/rag_experiment.yaml
```

### Generate Figures

```bash
python scripts/plot_results.py --results_dir results/
```

---

## Key Results (Preliminary)

| Method | Citation Accuracy | Recency Score | Hallucination Rate |
|--------|-------------------|---------------|-------------------|
| Frozen LLM (baseline) | — | — | — |
| LLM + RAG (Semantic Scholar) | — | — | — |

*Results to be filled after experiment execution.*

---

## Dataset

- **SemanticScholar Open Research Corpus (S2ORC)** — subset of AI/ML papers 2020–2026  
- **License:** ODC-BY  
- Access: https://api.semanticscholar.org/

---

## Dependencies

See `requirements.txt`. Primary libraries: `transformers`, `sentence-transformers`, `faiss-cpu`, `requests`, `pandas`, `matplotlib`.

---

## Responsible AI Disclosure

All AI assistance (Antigravity/Claude) is documented in `ai_assistance_log.md`. All results are from actual code execution. No results are fabricated.
