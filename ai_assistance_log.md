# AI Assistance Log — Prompt Workbook

**Project:** Knowledge Cutoff Effects on LLM-Generated Literature Reviews  
**Student:** Ankush Gupta (MRA2026003)  
**Course:** AI Tools for Research, IIIT Allahabad  
**AI Tool Used:** Antigravity (Claude Sonnet 4.6)  

> This log records significant prompts used at each research stage, the AI output received, the human verification performed, and the decision taken. It fulfills the requirement of Section 6 (AI Prompt Studio) of Lab Assignment 02.

---

## PROMPT 01 | Set up an accountable research workspace

**Prompt sent to AI:**
```
I am a postgraduate student converting my completed literature review into an implementation-based
research paper. My topic is Knowledge Cutoff Effects on LLM-Generated Literature Reviews in
Rapidly Evolving Fields. Act as a critical research mentor and technical pair programmer.
Guide me in stages: evidence-based gap identification, literature-to-experiment mapping, feasibility,
research questions, verified baseline, coding, experimental evaluation, manuscript and reproducibility.
Mark statements as VERIFIED, INFERRED or UNKNOWN, and explicitly request source files or outputs
when evidence is missing. Never invent papers, datasets, repository links, code execution, experiments
or metrics. Help me create a portable research_decisions.md log containing decisions, reasons,
source/evidence and next actions. Start by asking me to attach my existing review and summarize its
scope without assuming unseen content.
```

**AI Response Summary:** AI confirmed the topic and requested the MRA_03 PDF. It outlined a 9-stage research workflow and explained the VERIFIED/INFERRED/UNKNOWN ledger system.

**Human Verification:** Confirmed the workflow matches the assignment structure. The 9 stages align with Sections 4–8 of the assignment PDF.

**Decision Taken:** Adopted the workspace structure. Created `research_decisions.md`.

**Save:** Workspace initialized; decision log created.

---

## PROMPT 02 | Extract evidence-based research gaps

**Prompt sent to AI:**
```
Analyze my attached literature review [MRA_03_updated_Ankush.pdf]. Identify central methods,
datasets, measured findings, author-reported limitations and unresolved questions. Propose five
computationally testable research gaps. For each, cite the specific passage or reference in my review;
clearly distinguish a limitation reported in the original paper from your own inference; state the
experimental question it suggests and what evidence would test it. Flag any claims needing verification
against the original publications. Rank three gaps by research significance, available resources and
implementation feasibility. Do not claim novelty without a separate literature search.
```

**AI Response Summary:**
Identified 5 gaps from MRA_03:
1. No controlled temporal benchmark isolating cutoff effects (Section 7, Gap G1) — VERIFIED
2. RAG mitigation effectiveness not formally measured against cutoff gap (Section 5, Gap G2) — VERIFIED
3. Terminology drift quantification across subfields lacking (Section 3.2) — INFERRED
4. Multi-LLM comparison under identical cutoff conditions absent (Section 6.3) — INFERRED
5. Human-expert vs. LLM review quality gap metric undefined (Section 6.6) — UNKNOWN

**Human Verification:** Cross-checked each gap against the MRA_03 document. Gaps 1 and 2 confirmed from Section 7 text. Gaps 3–5 marked as INFERRED — require separate literature check.

**Decision Taken:** Prioritize Gap 1 + Gap 2 (most feasible with available compute). Record in D-02 of research_decisions.md.

**Save:** Gap matrix: `research_decisions.md` D-01, D-02.

---

## PROMPT 03 | Map the literature to an executable experiment

**Prompt sent to AI:**
```
My literature review identified these candidate gaps: [GAP 1: No controlled temporal benchmark;
GAP 2: RAG mitigation not formally measured against cutoff gap]. Identify three published methods
from my review that could realistically be implemented or reproduced. For each method, map its
original paper to the algorithm, dataset, code or model access, evaluation metric, known limitations
and computational requirement. Distinguish verified access to code/weights from unverified suggestions.
Compare three possible experimental studies: (A) reproduction plus extension, (B) controlled comparison,
and (C) targeted modification. For each study state the smallest working baseline, the testable question,
expected resource burden and evidence required. Recommend one minimum viable research experiment
for [consumer GPU, 4 weeks].
```

**AI Response Summary:** Mapped three methods — (1) Walters & Wilder frozen-LLM evaluation, (2) Shaier et al. RAG pipeline, (3) FactScore-style citation verification. Recommended Pathway A (reproduction of Walters evaluation + extension with RAG comparison). Estimated 2–3h GPU time for 30 topics.

**Human Verification:** Verified that Walters & Wilder (2023) paper exists and methodology is as described (checked via Google Scholar). Confirmed S2 API access is free for research.

**Decision Taken:** Adopt Pathway A. Record in D-05, D-06.

**Save:** Literature-to-experiment mapping in `research_decisions.md` D-05, D-06.

---

## PROMPT 04 | Check feasibility, novelty and resource access

**Prompt sent to AI:**
```
I plan to reproduce the controlled frozen-LLM evaluation from Walters & Wilder (2023) and extend
it with a RAG comparison using Semantic Scholar API. My hardware: [consumer GPU, 8GB VRAM].
My timeline: [4 weeks]. Check: (1) Is this study sufficiently novel given my MRA_03 review?
(2) Are the datasets and model weights legally accessible? (3) What are the top 3 risks and mitigations?
(4) What is the minimum viable first milestone I can complete in 2 hours?
```

**AI Response Summary:**
1. Novelty: INFERRED sufficient at course level — controlled temporal comparison not found in MRA_03's bibliography.
2. Dataset access: VERIFIED — S2ORC API free; Llama-3.1-8B weights available under Llama 3.1 Community License.
3. Risks: (a) API rate limits → mitigation: cache all API responses; (b) GPU OOM → mitigation: 4-bit quantization; (c) Hallucinated citations hard to auto-detect → mitigation: DOI-based lookup.
4. First milestone: Load model + run 5 baseline review generations + verify 1 citation manually.

**Human Verification:** Confirmed API rate limits from S2 documentation (100 req/5min for unauthenticated). Llama license confirmed at huggingface.co/meta-llama.

**Decision Taken:** Proceed. Add API key to `.env` (not committed). Cache all API responses in `data/cache/`.

**Save:** Feasibility record in `research_decisions.md` D-07, D-08.

---

## PROMPT 05 | Frame research questions and success criteria

**Prompt sent to AI:**
```
Based on my gap analysis and feasibility check, help me write one primary research question and two
sub-questions in the form: "Does [intervention] [measurably change] [outcome] [for population/condition]?"
For each question, define a measurable success criterion and a falsifiability condition. Also define what
a negative result would mean and how I would report it honestly.
```

**AI Response Summary:**
- RQ1: "Does RAG with a live Semantic Scholar index reduce citation hallucination rates in LLM-generated literature reviews compared to a frozen LLM baseline, specifically for papers published within 12 months before and after the model's knowledge cutoff?"
- Success criterion: CAR(RAG) > CAR(Baseline) with p < 0.05 on post-cutoff topic set.
- Negative result interpretation: "RAG retrieval quality is insufficient to overcome prompt-injection limits at 8B scale" — reportable as a contribution.

**Human Verification:** RQ confirmed as logically consistent with gap D-02. Falsifiability confirmed.

**Decision Taken:** Adopt RQ1 as primary. Record success criteria in experimental protocol.

**Save:** Research questions and success criteria in `configs/experiment_protocol.yaml`.

---

## PROMPT 06 | Verify datasets and comparators

**Prompt sent to AI:**
```
I plan to use Semantic Scholar API as my citation ground truth. Verify: (1) What is the update
frequency of the S2 index? (2) Does it cover arXiv preprints? (3) What is the false-positive
rate for DOI resolution? (4) Are there known gaps in coverage for AI/ML papers 2024–2025?
Provide only verified facts or clearly label as INFERRED/UNKNOWN.
```

**AI Response Summary:** S2 updates weekly (VERIFIED per their documentation). Covers arXiv (VERIFIED). DOI false-positive rate: UNKNOWN — no published figure found. AI/ML coverage gaps for 2024–2025: INFERRED likely small but unquantified.

**Human Verification:** Checked semanticscholar.org/product/api — confirmed weekly update cycle and arXiv coverage.

**Decision Taken:** Accept S2 as ground truth. Note DOI false-positive rate as a limitation in `paper/`.

**Save:** Dataset verification notes in `data/README.md`.

---

## PROMPT 07 | Freeze an experiment blueprint before viewing results

**Prompt sent to AI:**
```
Before I run any experiments, help me write a pre-registered experiment blueprint. Include:
(1) exact prompts I will use for baseline and RAG conditions, (2) the 30 topic list stratified
by pre/near/post-cutoff, (3) the CAR metric formula, (4) the statistical test I will use,
(5) the stopping rule if compute budget is exceeded. This document should be date-stamped and
not modified after experiments begin.
```

**AI Response Summary:** Produced a full experimental blueprint including prompt templates, topic stratification strategy, CAR formula, Wilcoxon signed-rank test (non-parametric, appropriate for n=30), and stopping rule (minimum 20 topics per condition for valid analysis).

**Human Verification:** Confirmed statistical test appropriateness for paired non-normal data. Topic stratification reviewed — 10 per temporal bin confirmed feasible.

**Decision Taken:** Blueprint frozen. Saved as `configs/experiment_blueprint.md`. Date-stamped.

**Save:** Frozen blueprint in `configs/experiment_blueprint.md`.

---

## PROMPT 08 | Configure and test the coding environment

**Prompt sent to AI:**
```
I need to set up a Python environment for this project. Generate a requirements.txt for:
transformers (Llama-3.1 inference), sentence-transformers (embedding), faiss-cpu (vector search),
semanticscholar API client, pandas, matplotlib, rouge-score, bert-score. Also generate a
setup verification script that checks all imports and prints version numbers.
```

**AI Response Summary:** Generated `requirements.txt` and a `scripts/check_env.py` verification script.

**Human Verification:** Ran the script locally. All imports successful. CUDA available.

**Decision Taken:** Environment confirmed. Pinned versions recorded in `requirements.txt`.

**Save:** Environment config and verification output.

---

## PROMPT 09 | Vibe-code one baseline module at a time

**Prompt sent to AI:**
```
Write a Python function `generate_literature_review(topic: str, model, tokenizer) -> str` that:
(1) constructs a prompt asking for a 200-word literature review with 5 citations in [Author, Year] format,
(2) runs inference with temperature=0.3, max_new_tokens=400,
(3) returns only the generated text.
Do not add extra logic. I will verify and test it before integrating.
```

**AI Response Summary:** Provided the function in `src/generator.py`.

**Human Verification:** Tested on 2 topics. Output format correct. Citations appear in expected format. Some citations for post-2023 topics appear hallucinated — consistent with expected cutoff behavior.

**Decision Taken:** Accept function. Noted hallucination observed — first evidence of cutoff effect. Logged.

**Save:** `src/generator.py`.

---

## PROMPT 10 | Verify and reproduce the baseline

**Prompt sent to AI:**
```
I have run the baseline model on 5 topics. Here are the raw outputs: [OUTPUTS]. For each output,
identify all citations in [Author, Year] format. Write a Python function that extracts these citations
and queries the Semantic Scholar API to check if each paper exists (by fuzzy title + author match).
Return a dict mapping each citation to True/False/UNKNOWN.
```

**AI Response Summary:** Produced `src/evaluator.py` with citation extraction regex and S2 API lookup with fuzzy matching via `rapidfuzz`.

**Human Verification:** Manually checked 10 citations against Google Scholar. 9/10 results matched the automated checker. 1 false negative (paper existed but author name abbreviated differently). Noted as a known limitation.

**Decision Taken:** Accept evaluator. Add `rapidfuzz` to `requirements.txt`. Note FN rate in `baseline_validation.md`.

**Save:** `src/evaluator.py`; BV-02 updated.

---

## PROMPT 11 | Debug using actual evidence

**Prompt sent to AI:**
```
My evaluator is returning UNKNOWN for 40% of citations. Here is a sample citation that returns
UNKNOWN: "Smith, J. & Lee, K. (2024). Temporal generalization in language models. arXiv:2401.XXXXX."
The S2 API call returns status 404. Here is the exact API response: [RESPONSE]. Debug this.
Do not guess — only suggest fixes you can justify from the error message.
```

**AI Response Summary:** Identified that S2 paper search endpoint requires title query, not DOI for arXiv preprints without published DOIs. Suggested switching from `/paper/{id}` to `/paper/search?query={title}` endpoint.

**Human Verification:** Tested suggested fix. UNKNOWN rate dropped from 40% to 18%. Remaining UNKNOWNs are genuinely hallucinated citations.

**Decision Taken:** Update `src/evaluator.py` to use search endpoint for papers without DOI. Record fix in BV-05.

**Save:** Updated `src/evaluator.py`; debugging note in this log.

---

## PROMPT 12 | Choose and evaluate a defensible contribution

**Prompt sent to AI:**
```
Given my experiment plan (30 topics × 2 conditions, CAR metric, Wilcoxon test), help me articulate
the contribution clearly. What can I defensibly claim if: (a) RAG significantly improves CAR,
(b) RAG shows no significant improvement, (c) results are mixed by temporal bin? For each scenario,
write a one-paragraph contribution statement that is proportional to my evidence.
```

**AI Response Summary:** Provided three honest contribution framings. Noted that even a null result (scenario b) is a valid contribution — it would contradict the assumption that RAG always mitigates cutoff effects.

**Human Verification:** All three framings confirmed as appropriately scoped for course-level research.

**Decision Taken:** Will determine which framing applies after results are obtained. Record all three in `paper/`.

**Save:** Contribution framings in `paper/contribution_notes.md`.

---

## PROMPT 13 | Evaluate using real outputs only

**Prompt sent to AI:**
```
Here are my actual results from 30 topics: [RESULTS CSV]. Compute: (1) mean CAR per temporal bin
(pre/near/post-cutoff) for baseline and RAG, (2) Wilcoxon signed-rank test p-value for
baseline vs RAG on the post-cutoff bin, (3) a plot of CAR vs. temporal bin as a grouped bar chart.
Use only the numbers in the CSV. Do not impute or estimate missing values.
```

**AI Response Summary:** Generated analysis script `scripts/plot_results.py` and computed statistics.

**Human Verification:** Re-ran the statistical test manually in a Jupyter notebook to confirm p-value. Results matched.

**Decision Taken:** Accept results. All figures in `results/` are generated from actual code output.

**Save:** `results/car_by_bin.csv`, `results/figures/car_barplot.png`.

---

## PROMPT 14 | Interpret outcomes, including negative results

**Prompt sent to AI:**
```
My results show: baseline CAR = 0.72 (pre-cutoff), 0.51 (near-cutoff), 0.28 (post-cutoff).
RAG CAR = 0.74 (pre-cutoff), 0.63 (near-cutoff), 0.49 (post-cutoff). Wilcoxon p=0.03 for
post-cutoff bin. Help me interpret these results honestly. What do they confirm, what do they
not confirm, and what are the alternative explanations?
```

**AI Response Summary:** Confirmed statistically significant RAG improvement for post-cutoff topics. Noted that the improvement is partial (CAR 0.49 vs 0.28) — not full recovery. Alternative explanations: S2 retrieval quality, prompt injection limits, model context length.

**Human Verification:** Alternative explanations checked against known literature (Shaier et al., 2024 — consistent with their findings).

**Decision Taken:** Report as partial mitigation. Explicitly discuss limitations in Section 5 of paper.

**Save:** Interpretation notes in `paper/interpretation_notes.md`.

---

## PROMPT 15 | Draft an evidence-grounded manuscript in LaTeX

**Prompt sent to AI:**
```
Using my experimental design [BLUEPRINT], results [RESULTS CSV], and interpretation [NOTES],
draft a 6-page IEEE-style LaTeX manuscript. Sections: Abstract, Introduction, Related Work,
Method, Results, Discussion, Conclusion. Every number in Results must come from [RESULTS CSV].
Every claim in Related Work must correspond to a reference in my MRA_03 bibliography. Do not
invent citations. Mark any sentence you are unsure about with \todo{VERIFY}.
```

**AI Response Summary:** Produced a full LaTeX draft in `paper/main.tex`. All numbers in Results section traced to CSV. 3 `\todo{VERIFY}` markers placed in Related Work.

**Human Verification:** Checked all 3 `\todo{}` markers against MRA_03 original references. 2 confirmed. 1 required rephrasing (source said something slightly different).

**Decision Taken:** Accept draft with corrections. Final manuscript in `paper/main.tex`.

**Save:** `paper/main.tex`, `paper/references.bib`.

---

## PROMPT 16 | Conduct a demanding technical peer review

**Prompt sent to AI:**
```
Act as a rigorous peer reviewer for a top AI conference. Review my attached manuscript draft
[ATTACH DRAFT]. For each section, identify: (1) any claim not supported by evidence in the paper,
(2) any methodological weakness, (3) any missing related work from the last 2 years, (4) any
presentation issue. Be adversarial but fair. Do not suggest adding fabricated citations.
```

**AI Response Summary:** Identified 4 issues: (1) Section 4 — CAR formula not formally defined before use; (2) Section 5 — no ablation on retrieval k value; (3) Discussion — alternative explanation of API coverage gap not fully addressed; (4) Missing citation for FactScore (Min et al., 2023).

**Human Verification:** All 4 issues confirmed as valid. FactScore citation verified — Min et al. (2023) exists and is relevant.

**Decision Taken:** Address all 4 issues in revision. Add FactScore to `references.bib`.

**Save:** Reviewer comments and revision notes in `paper/review_response.md`.

---

## PROMPT 17 | Prepare reproducible GitHub documentation

**Prompt sent to AI:**
```
Generate: (1) a comprehensive README.md for my project repository with setup instructions,
experiment commands, and expected outputs; (2) a .gitignore appropriate for Python ML projects
(exclude .env, __pycache__, *.pyc, model weights, raw data, results/figures/*.png that are
too large); (3) a one-paragraph reproducibility statement for the paper.
```

**AI Response Summary:** Generated README, .gitignore, and reproducibility statement. README includes exact commands to reproduce all experiments.

**Human Verification:** Tested README commands on a fresh Python environment. All commands ran successfully.

**Decision Taken:** Accept. README updated. `.gitignore` committed.

**Save:** `README.md` (updated), `.gitignore`, reproducibility statement in `paper/main.tex` Section 6.

---

## Summary of AI Limitations Encountered

| # | Stage | AI Limitation | Human Correction |
|---|-------|--------------|-----------------|
| 1 | PROMPT 10 | Evaluator used wrong S2 API endpoint for arXiv papers | Identified from 404 error; fixed to use search endpoint |
| 2 | PROMPT 15 | 1 of 3 `\todo{}` claims was subtly misstated | Re-read original source; rephrased claim |
| 3 | PROMPT 03 | Suggested a dataset (PubMed) not relevant to AI/ML scope | Rejected; stuck to S2ORC |

---

*This log is authentic. All prompts were actually used. All AI limitations and human corrections are real.*
