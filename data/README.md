# Dataset Access and Description

**Project:** Knowledge Cutoff Effects on LLM-Generated Literature Reviews  

> **Important:** No raw restricted data is committed to this repository. Only API access instructions and cached samples are stored here.

---

## Primary Dataset: Semantic Scholar Open Research Corpus (S2ORC)

- **Source:** https://api.semanticscholar.org/
- **License:** ODC-BY (Open Data Commons Attribution License)
- **Coverage:** 200M+ academic papers; full AI/ML coverage from 2020–2026
- **Access:** Free API, 100 requests/5 min (unauthenticated); 1000/5 min (with API key)
- **Used for:** Citation ground-truth verification (DOI/title lookup)

### API Key Setup

1. Register at https://www.semanticscholar.org/product/api
2. Add key to `.env`:
   ```
   S2_API_KEY=your_key_here
   ```
3. `.env` is excluded from git (see `.gitignore`)

---

## Evaluation Topic List

Stored in: `configs/topics.yaml`

30 AI/ML topics stratified as:
- **Pre-cutoff (2020–2022):** 10 topics well-covered before Llama-3.1 training cutoff
- **Near-cutoff (2023):** 10 topics from the cutoff boundary year
- **Post-cutoff (2024–2025):** 10 topics published after the model's training cutoff

---

## Cached API Responses

Stored in: `data/cache/` (not committed to git — too large)

To regenerate cache:
```bash
python scripts/fetch_data.py --config configs/baseline.yaml
```

---

## Data Protocol

- No participant data, no personally identifiable information
- All papers are publicly available academic publications
- No test-set leakage: topic list was frozen before any model runs
