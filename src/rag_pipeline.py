"""
src/rag_pipeline.py
RAG pipeline: retrieves relevant papers from Semantic Scholar API and injects
them as context for literature review generation.
Author: Ankush Gupta (MRA2026003)
"""

import os
import time
import requests
from typing import List, Optional

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
S2_API_KEY = os.getenv("S2_API_KEY", "")


def retrieve_papers(
    query: str,
    top_k: int = 5,
    year_min: int = 2020,
    year_max: int = 2026,
) -> List[dict]:
    """
    Retrieve top-k relevant papers from Semantic Scholar for a given query.

    Returns:
        List of paper dicts with keys: title, authors, year, abstract.
    """
    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY

    params = {
        "query": query,
        "limit": top_k * 2,  # Over-fetch to filter by year
        "fields": "title,authors,year,abstract",
        "year": f"{year_min}-{year_max}",
    }

    try:
        resp = requests.get(
            f"{S2_API_BASE}/paper/search",
            params=params,
            headers=headers,
            timeout=15,
        )
        if resp.status_code != 200:
            return []

        data = resp.json()
        papers = data.get("data", [])

        # Filter: must have abstract and year
        filtered = [
            p for p in papers
            if p.get("abstract") and p.get("year") and year_min <= p["year"] <= year_max
        ]
        return filtered[:top_k]

    except requests.RequestException:
        return []


def format_retrieved_papers(papers: List[dict]) -> str:
    """Format retrieved papers into a context string for the LLM prompt."""
    if not papers:
        return "No relevant recent papers found."

    lines = []
    for i, p in enumerate(papers, 1):
        authors = ", ".join(a.get("name", "") for a in p.get("authors", [])[:3])
        year = p.get("year", "unknown")
        title = p.get("title", "Untitled")
        abstract = (p.get("abstract", "") or "")[:300]
        lines.append(f"{i}. {authors} ({year}). {title}.\n   Abstract: {abstract}...")

    return "\n\n".join(lines)


def rag_retrieve_and_format(topic: str, top_k: int = 5) -> str:
    """
    Full RAG retrieval pipeline for a given topic.

    Returns:
        Formatted context string to inject into LLM prompt.
    """
    papers = retrieve_papers(topic, top_k=top_k)
    time.sleep(0.5)  # Rate limit respect
    return format_retrieved_papers(papers)
