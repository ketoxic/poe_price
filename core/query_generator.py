# core/query_generator.py

from typing import List, Dict
from core.query_builder import build_query


def generate_queries(
    flasks: List[str],
    prefixes: List[Dict],
    suffixes: List[Dict]
) -> List[Dict]:
    """
    Generate F × P × S queries
    """
    queries = []

    for flask in flasks:
        for prefix in prefixes:
            for suffix in suffixes:
                queries.append({
                    "flask": flask,
                    "prefix_id": prefix["id"],
                    "suffix_id": suffix["id"],
                    "query": build_query(flask, prefix, suffix)
                })

    return queries
