"""
src/evaluator.py
Evaluates Citation Accuracy Rate (CAR) by verifying generated citations against
the Semantic Scholar API.
Author: Ankush Gupta (MRA2026003)
"""

import re
import os
import time
import requests
from typing import Dict, List, Tuple

S2_API_BASE = "https://api.semanticscholar.org/graph/v1"
S2_API_KEY = os.getenv("S2_API_KEY", "")


def extract_citations(text: str) -> List[str]:
    """
    Extract citations in [Author et al., Year] or [Author & Author, Year] format.

    Returns:
        List of raw citation strings.
    """
    pattern = r'\[([A-Z][a-zA-Z\-]+(?:\s+et\s+al\.?|(?:\s+&\s+[A-Z][a-zA-Z\-]+)?)),\s*(\d{4}[a-z]?)\]'
    matches = re.findall(pattern, text)
    return [f"{author}, {year}" for author, year in matches]


def lookup_citation_s2(citation: str, retries: int = 2) -> str:
    """
    Look up a citation string against Semantic Scholar API.

    Returns:
        "VERIFIED" | "NOT_FOUND" | "UNKNOWN"
    """
    headers = {}
    if S2_API_KEY:
        headers["x-api-key"] = S2_API_KEY

    # Extract year for filtering
    year_match = re.search(r'\d{4}', citation)
    year = year_match.group() if year_match else None

    # Build query: use author name + year
    author_part = re.sub(r',?\s*\d{4}[a-z]?', '', citation).strip()
    query = f"{author_part} {year}" if year else author_part

    for attempt in range(retries + 1):
        try:
            resp = requests.get(
                f"{S2_API_BASE}/paper/search",
                params={"query": query, "limit": 5, "fields": "title,authors,year"},
                headers=headers,
                timeout=10,
            )
            if resp.status_code == 429:
                time.sleep(5)
                continue
            if resp.status_code != 200:
                return "UNKNOWN"

            data = resp.json()
            papers = data.get("data", [])
            if not papers:
                return "NOT_FOUND"

            # Check if any result matches the year
            for paper in papers:
                if year and str(paper.get("year", "")) == year:
                    return "VERIFIED"
            # Year mismatch — citation may be hallucinated
            return "NOT_FOUND"

        except requests.RequestException:
            time.sleep(2)

    return "UNKNOWN"


def compute_car(generated_text: str) -> Tuple[float, Dict[str, str]]:
    """
    Compute Citation Accuracy Rate for a generated literature review.

    Returns:
        (car_score, citation_status_dict)
    """
    citations = extract_citations(generated_text)
    if not citations:
        return 0.0, {}

    statuses: Dict[str, str] = {}
    for citation in citations:
        status = lookup_citation_s2(citation)
        statuses[citation] = status
        time.sleep(0.5)  # Respect rate limits

    verified = sum(1 for s in statuses.values() if s == "VERIFIED")
    total = len(statuses)
    car = verified / total if total > 0 else 0.0

    return car, statuses
