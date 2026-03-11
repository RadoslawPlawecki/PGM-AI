"""
@author: Radosław Pławecki
"""

import pandas as pd

def abundance_validator(df, tol: float=1) -> None:
    """
    Remove rows where bacterial abundances do not sum to ~1 or ~100.
    """
    row_sums = df.iloc[:, 2:].sum(axis=1)
    median_sum = row_sums.median()
    target = 1 if abs(median_sum - 1) < abs(median_sum - 100) else 100
    valid_rows = (row_sums - target).abs() < tol
    removed = (~valid_rows).sum()
    if removed > 0:
        print(f"[WARNING] {removed} rows removed because of invalid abundance sums.")
    else:
        print(f"[INFO] All rows have valid abundance sums (≈{target}).")
    return df.loc[valid_rows].reset_index(drop=True)


def parse_taxonomy(tax_lin: str):
    """
    Parse a taxonomic lineage string into a dictionary of taxonomic ranks.
    """
    rank_map = {
        "k": "kingdom",
        "p": "phylum",
        "c": "class",
        "o": "order",
        "f": "family",
        "g": "genus",
        "s": "species"
    }
    result = {}
    for part in tax_lin.split("|"):
        prefix, name = part.split("__", 1)
        rank = rank_map.get(prefix)
        if rank:
            result[rank] = name
    return result
