# Baseline Validation Report

**Project:** Knowledge Cutoff Effects on LLM-Generated Literature Reviews  
**Student:** Ankush Gupta (MRA2026003)  

---

## Purpose

This document records all reproduction checks performed before comparing the RAG-enhanced pipeline against the frozen LLM baseline. Any deviation from expected behaviour is documented here.

---

## BV-01 | Model Loading Check

**Task:** Verify that `meta-llama/Llama-3.1-8B-Instruct` loads and generates coherent text.  
**Command:**
```python
from transformers import AutoModelForCausalLM, AutoTokenizer
model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-3.1-8B-Instruct", load_in_4bit=True)
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-3.1-8B-Instruct")
```
**Expected:** Model loads without error; generates a coherent sentence when prompted.  
**Result:** [ TO BE FILLED AFTER EXECUTION ]  
**Status:** ☐ PASS  ☐ FAIL  ☐ DEVIATION NOTED

---

## BV-02 | Citation Accuracy Rate (CAR) on Known Topic

**Task:** Run baseline on the topic "Retrieval-Augmented Generation (RAG)" — a topic well-covered before the LLM cutoff — and check CAR.  
**Expected:** CAR ≥ 0.70 (topic well within cutoff; references should be largely correct).  
**Result:** [ TO BE FILLED ]  
**Status:** ☐ PASS  ☐ FAIL

---

## BV-03 | CAR on Post-Cutoff Topic

**Task:** Run baseline on "LLM knowledge cutoff benchmark datasets (2024–2025)" — post-cutoff topic.  
**Expected:** CAR significantly lower (≤ 0.30), confirming cutoff-driven degradation.  
**Result:** [ TO BE FILLED ]  
**Status:** ☐ PASS  ☐ FAIL

---

## BV-04 | Semantic Scholar API Connectivity

**Task:** Confirm API returns paper metadata for a known paper DOI.  
**Command:**
```python
import requests
r = requests.get("https://api.semanticscholar.org/graph/v1/paper/DOI:10.1145/3626772.3657743")
assert r.status_code == 200
```
**Result:** [ TO BE FILLED ]  
**Status:** ☐ PASS  ☐ FAIL

---

## BV-05 | RAG Retrieval Sanity Check

**Task:** Confirm RAG retrieves ≥ 3 relevant papers for a standard topic query.  
**Result:** [ TO BE FILLED ]  
**Status:** ☐ PASS  ☐ FAIL

---

## Deviations

| ID | Description | Resolution |
|----|-------------|------------|
| — | None yet | — |

---

## Sign-off

Before proceeding to full experiments, BV-01 through BV-05 must all PASS or have documented resolutions.  
**Sign-off date:** [ TO BE FILLED ]
