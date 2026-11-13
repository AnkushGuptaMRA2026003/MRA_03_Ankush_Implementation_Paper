# Research Decisions Log

**Project:** Knowledge Cutoff Effects on LLM-Generated Literature Reviews  
**Student:** Ankush Gupta (MRA2026003)  
**Course:** AI Tools for Research, IIIT Allahabad  

---

## Decision Log Format

Each entry records: **Decision → Reason → Source/Evidence → Next Action**

---

## D-01 | Research Area Continuity

**Decision:** Continue in the LLM knowledge-cutoff domain from MRA_03 literature review.  
**Reason:** The review (MRA_03) already maps the gap space and identifies unanswered quantitative questions about cutoff-to-quality degradation curves.  
**Evidence:** VERIFIED — MRA_03 Section 6.6 explicitly lists "lack of controlled temporal experiments" as a gap. Original papers (Shaier et al., 2024; Walters & Wilder, 2023) confirm no controlled variable-cutoff benchmark exists.  
**Next Action:** Narrow to one tractable question (citation accuracy vs. time-lag).

---

## D-02 | Research Question Selection

**Decision:** Primary RQ — "Does RAG with a live academic index reduce citation hallucination rates compared to a frozen LLM baseline, and by how much as a function of paper publication recency?"  
**Reason:** Directly addresses the gap identified in MRA_03 Section 7 (open problem: "mitigation effectiveness not formally measured against cutoff gap").  
**Evidence:** VERIFIED from MRA_03 bibliography entries [5,8] — RAG systems described but no controlled temporal comparison performed.  
**Next Action:** Select open-source LLM and academic API for RAG.

---

## D-03 | Model Selection

**Decision:** Use `meta-llama/Llama-3.1-8B-Instruct` (HuggingFace) as the frozen LLM baseline.  
**Reason:** Knowledge cutoff is publicly documented (early 2023). Open weights. Fits on consumer GPU (≤16 GB VRAM with 4-bit quant).  
**Evidence:** VERIFIED — HuggingFace model card confirms training data cutoff. License: Llama 3.1 Community License (non-commercial research use permitted).  
**Status:** INFERRED that 8B scale is sufficient for literature review generation — needs empirical check.  
**Next Action:** Run environment sanity check; generate 5 test reviews and inspect outputs.

---

## D-04 | Dataset / Evaluation Corpus Selection

**Decision:** Use Semantic Scholar Open Research Corpus (S2ORC) AI/ML subset, filtered to papers 2022–2026, as the ground-truth citation pool.  
**Reason:** Legally accessible (ODC-BY), API available, covers the temporal range that spans the LLM cutoff boundary.  
**Evidence:** VERIFIED — https://www.semanticscholar.org/product/api (confirmed public access, no restricted data needed).  
**Next Action:** Write `data/fetch_s2orc.py` to pull 500 AI/ML abstracts from 2022–2026 via API.

---

## D-05 | Baseline Design

**Decision:** Baseline = frozen LLM prompted with a research topic; no external retrieval.  
**Metric = Citation Accuracy Rate (CAR):** fraction of generated citations that resolve to real, correctly attributed papers via S2 API lookup.  
**Reason:** CAR is objective, automated, and directly measures cutoff-driven hallucination.  
**Evidence:** INFERRED from Walters & Wilder (2023) methodology — they use manual verification; we automate via API.  
**Next Action:** Implement `src/evaluator.py` with CAR metric.

---

## D-06 | RAG Design

**Decision:** RAG pipeline = Semantic Scholar API retrieval (top-k=5 by keyword + date filter) → inject abstracts as context → LLM generation.  
**Reason:** Minimal implementation, reproduces the RAG pattern from MRA_03 Section 5.  
**Evidence:** INFERRED — exact retrieval quality depends on API; requires empirical validation.  
**Next Action:** Implement `src/rag_pipeline.py`; run on 10 topics and compare CAR.

---

## D-07 | Evaluation Protocol

**Decision:** 30 topics drawn from AI/ML subfields (10 pre-cutoff, 10 near-cutoff, 10 post-cutoff). Each topic evaluated in both Baseline and RAG conditions. Metrics: CAR, Recency Score (mean publication year of cited papers), Hallucination Rate (1 - CAR).  
**Reason:** Three temporal bins allow plotting degradation curve. 30 topics is feasible within compute budget.  
**Evidence:** VERIFIED design — aligns with controlled comparison (Pathway A/B).  
**Next Action:** Create topic list in `configs/topics.yaml`.

---

## D-08 | Compute Resources

**Hardware:** NVIDIA GPU (≥8 GB VRAM) or Google Colab T4.  
**Time estimate:** ~2h for 30 topics × 2 conditions with 8B 4-bit model.  
**Fallback:** Use `gpt-3.5-turbo` via OpenAI API if local inference fails.  
**Evidence:** INFERRED — based on typical Llama-3 inference throughput.
