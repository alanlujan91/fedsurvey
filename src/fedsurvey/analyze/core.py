"""Core analysis functions for SCF data."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fedsurvey.core.exceptions import ProcessingError
from fedsurvey.utils.stats import weighted_quantile

if TYPE_CHECKING:
    import pandas as pd


def calculate_percentiles(
    df: pd.DataFrame,
    variable: str,
    weights: str | None = "wgt",
    percentiles: list[float] | None = None,
) -> dict[float, float]:
    """Calculate weighted percentiles for a variable."""
    if percentiles is None:
        percentiles = [10, 25, 50, 75, 90]
    try:
        if weights is None:
            return {p: df[variable].quantile(p / 100) for p in percentiles}

        return {
            p: weighted_quantile(df[variable], df[weights], p / 100)
            for p in percentiles
        }
    except Exception as e:
        msg = f"Error calculating percentiles: {e}"
        raise ProcessingError(msg)


def calculate_concentration(
    df: pd.DataFrame,
    variable: str,
    weight_col: str = "wgt",
    thresholds: list[float] | None = None,
) -> dict[str, float]:
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
    if thresholds is None:
        thresholds = [0.01, 0.1, 0.5]
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
        msg = f"Error calculating concentration: {e}"
        raise ProcessingError(msg)
