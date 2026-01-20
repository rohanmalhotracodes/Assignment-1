#!/usr/bin/env python3
import math
import os
import sys
from typing import List, Tuple

import pandas as pd


def _die(msg: str, code: int = 1) -> None:
    print(msg)
    sys.exit(code)


def _parse_weights_impacts(weights_s: str, impacts_s: str) -> Tuple[List[float], List[str]]:
    if "," not in weights_s or "," not in impacts_s:
        _die("Error: Impacts and weights must be separated by ',' (comma).")

    weights_raw = [w.strip() for w in weights_s.split(",") if w.strip() != ""]
    impacts_raw = [i.strip() for i in impacts_s.split(",") if i.strip() != ""]

    try:
        weights = [float(w) for w in weights_raw]
    except ValueError:
        _die("Error: Weights must be numeric values separated by commas.")

    impacts = impacts_raw
    for imp in impacts:
        if imp not in ["+", "-"]:
            _die("Error: Impacts must be either '+' or '-' separated by commas.")

    return weights, impacts


def _validate_input_df(df: pd.DataFrame) -> None:
    if df.shape[1] < 3:
        _die("Error: Input file must contain three or more columns.")

    # From 2nd to last must be numeric
    crit = df.iloc[:, 1:]
    for col in crit.columns:
        # try convert to numeric; if any non-numeric -> error
        coerced = pd.to_numeric(crit[col], errors="coerce")
        if coerced.isna().any():
            _die("Error: From 2nd to last columns must contain numeric values only.")


def topsis(df: pd.DataFrame, weights: List[float], impacts: List[str]) -> pd.DataFrame:
    # Work on a copy
    out = df.copy()

    crit = out.iloc[:, 1:].apply(pd.to_numeric)
    n_criteria = crit.shape[1]

    if len(weights) != n_criteria or len(impacts) != n_criteria:
        _die(
            "Error: The number of weights, impacts and number of columns (from 2nd to last) must be the same."
        )

    # Normalize
    denom = (crit ** 2).sum(axis=0).apply(math.sqrt)
    denom = denom.replace(0, 1.0)  # avoid divide-by-zero
    norm = crit / denom

    # Weight
    w = pd.Series(weights, index=crit.columns, dtype=float)
    weighted = norm * w

    # Ideal best/worst
    ideal_best = pd.Series(index=crit.columns, dtype=float)
    ideal_worst = pd.Series(index=crit.columns, dtype=float)
    for col, imp in zip(crit.columns, impacts):
        if imp == "+":
            ideal_best[col] = weighted[col].max()
            ideal_worst[col] = weighted[col].min()
        else:
            ideal_best[col] = weighted[col].min()
            ideal_worst[col] = weighted[col].max()

    # Distances
    d_best = ((weighted - ideal_best) ** 2).sum(axis=1).apply(math.sqrt)
    d_worst = ((weighted - ideal_worst) ** 2).sum(axis=1).apply(math.sqrt)

    score = d_worst / (d_best + d_worst)
    out["Topsis Score"] = score

    # Rank: higher score is better
    out["Rank"] = out["Topsis Score"].rank(ascending=False, method="dense").astype(int)
    return out


def main(argv: List[str]) -> None:
    if len(argv) != 5:
        _die(
            "Error: Correct number of parameters required.\n"
            "Usage: python topsis.py <InputDataFile> <Weights> <Impacts> <OutputResultFileName>"
        )

    _, input_path, weights_s, impacts_s, output_path = argv

    if not os.path.isfile(input_path):
        _die("Error: File not Found")

    try:
        df = pd.read_csv(input_path)
    except Exception:
        _die("Error: Unable to read input file. Ensure it is a valid CSV.")

    _validate_input_df(df)
    weights, impacts = _parse_weights_impacts(weights_s, impacts_s)

    result = topsis(df, weights, impacts)

    try:
        result.to_csv(output_path, index=False)
    except Exception:
        _die("Error: Unable to write output file.")

    print(f"Success: Result written to {output_path}")


if __name__ == "__main__":
    main(sys.argv)
