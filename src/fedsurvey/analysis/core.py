"""Core analysis functions for SCF data."""

from __future__ import annotations

from typing import Dict, List, Optional

import pandas as pd

from ..exceptions import ProcessingError
from ..utils.stats import weighted_quantile


def calculate_percentiles(
    df: pd.DataFrame,
    variable: str,
    weights: Optional[str] = "wgt",
    percentiles: List[float] = [10, 25, 50, 75, 90],
) -> Dict[float, float]:
    """Calculate weighted percentiles for a variable."""
    try:
        if weights is None:
            return {p: df[variable].quantile(p / 100) for p in percentiles}

        return {
            p: weighted_quantile(df[variable], df[weights], p / 100)
            for p in percentiles
        }
    except Exception as e:
        raise ProcessingError(f"Error calculating percentiles: {e}")


def calculate_concentration(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "wgt",
    thresholds: List[float] = [0.01, 0.1, 0.5],
) -> Dict[str, float]:
    """Calculate concentration metrics (e.g., top 1% share).

    Args:
    ----
        df: DataFrame containing SCF data
        variable: Variable to analyze concentration
        weight_col: Name of weight column
        thresholds: List of thresholds (e.g., [0.01] for top 1%)

    Returns:
    -------
        Dictionary with top share values
    """
    try:
        df = df.copy()
        total = (df[variable] * df[weight_col]).sum()
        shares = {}

        # Sort by variable value in descending order
        df = df.sort_values(variable, ascending=False)

        # Calculate cumulative weighted shares
        df["cum_weight"] = (df[weight_col]).cumsum()
        df["cum_weight_pct"] = df["cum_weight"] / df[weight_col].sum()

        for pct in thresholds:
            # Find cutoff point where cumulative weight exceeds threshold
            cutoff_idx = df["cum_weight_pct"].searchsorted(pct)

            # Calculate share held by top group
            top_share = (
                df.iloc[:cutoff_idx][variable] * df.iloc[:cutoff_idx][weight_col]
            ).sum() / total

            shares[f"top_{int(pct*100)}"] = top_share

        return shares

    except Exception as e:
        raise ProcessingError(f"Error calculating concentration: {e}")
