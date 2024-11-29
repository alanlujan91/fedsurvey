"""Utilities for handling SCF survey weights."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fedsurvey.exceptions import ProcessingError

if TYPE_CHECKING:
    import pandas as pd


def apply_replicate_weights(
    df: pd.DataFrame,
    weight_col: str = "wgt",
    replicate_factor: int = 5,
) -> pd.DataFrame:
    """Apply replicate weight adjustments from bulletin macro.

    Args:
    ----
        df: DataFrame containing SCF data
        weight_col: Name of weight column
        replicate_factor: Number of implicates (default 5)

    Returns:
    -------
        DataFrame with adjusted weights

    """
    try:
        df = df.copy()
        df[f"{weight_col}_adj"] = df[weight_col] / replicate_factor
        return df
    except Exception as e:
        msg = f"Error applying replicate weights: {e}"
        raise ProcessingError(msg)


def adjust_influential_weights(
    df: pd.DataFrame,
    threshold: float = 0.015,  # 1.5% as used in bulletin
    measures: list[str] | None = None,
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Adjust weights to dampen influence of extreme cases.

    Args:
    ----
        df: DataFrame containing SCF data
        threshold: Maximum allowed share of total (default 0.015)
        measures: Variables to check for influence
        weight_col: Name of weight column

    Returns:
    -------
        DataFrame with adjusted weights

    """
    if measures is None:
        measures = ["networth", "fin", "nfin", "debt"]
    try:
        df = df.copy()
        totals = {m: (df[m] * df[weight_col]).sum() for m in measures}

        for measure in measures:
            shares = df[measure] * df[weight_col] / totals[measure]
            mask = shares > threshold
            if mask.any():
                df.loc[mask, weight_col] *= threshold / shares[mask]

        return df
    except Exception as e:
        msg = f"Error adjusting influential weights: {e}"
        raise ProcessingError(msg)
