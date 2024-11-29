"""Utilities for computing statistics."""

from __future__ import annotations

import numpy as np
import pandas as pd
from statsmodels.stats.weightstats import DescrStatsW


def compute_means(group: pd.DataFrame) -> pd.DataFrame:
    """Compute weighted means for a group.

    Args:
    ----
        group: DataFrame containing group data

    Returns:
    -------
        DataFrame with weighted means

    """
    year = group["age_lbl"].iloc[0]
    race_lbl = group["race_lbl"].iloc[0]
    weights = group["wgt"]

    # Handle missing values by computing on non-missing data only
    fin_data = group["fin"].dropna()
    fin_weights = weights[fin_data.index] if not fin_data.empty else weights
    stats_fin = (
        DescrStatsW(fin_data, weights=fin_weights) if not fin_data.empty else None
    )

    hequity_data = group["hequity"].dropna()
    hequity_weights = weights[hequity_data.index] if not hequity_data.empty else weights
    stats_hequity = (
        DescrStatsW(hequity_data, weights=hequity_weights)
        if not hequity_data.empty
        else None
    )

    # Only compute equity/fin ratio for positive home equity
    mask = (group["hequity"] > 0) & group["equityfin"].notna()
    equityfin_data = group["equityfin"][mask]
    equityfin_weights = weights[mask]
    stats_equityfin = (
        DescrStatsW(equityfin_data, weights=equityfin_weights)
        if not equityfin_data.empty
        else None
    )

    return pd.DataFrame(
        {
            "age_lbl": [year],
            "race_lbl": [race_lbl],
            "fin": [stats_fin.mean if stats_fin else np.nan],
            "hequity": [stats_hequity.mean if stats_hequity else np.nan],
            "equityfin": [stats_equityfin.mean if stats_equityfin else np.nan],
        },
    )


def compute_medians(group: pd.DataFrame) -> pd.DataFrame:
    """Compute weighted medians for a group.

    Args:
    ----
        group: DataFrame containing group data

    Returns:
    -------
        DataFrame with weighted medians

    """
    year = group["age_lbl"].iloc[0]
    race_lbl = group["race_lbl"].iloc[0]
    weights = group["wgt"]

    # Handle missing values by computing on non-missing data only
    fin_data = group["fin"].dropna()
    fin_weights = weights[fin_data.index] if not fin_data.empty else weights
    stats_fin = (
        DescrStatsW(fin_data, weights=fin_weights) if not fin_data.empty else None
    )

    hequity_data = group["hequity"].dropna()
    hequity_weights = weights[hequity_data.index] if not hequity_data.empty else weights
    stats_hequity = (
        DescrStatsW(hequity_data, weights=hequity_weights)
        if not hequity_data.empty
        else None
    )

    # Only compute equity/fin ratio for positive home equity
    mask = (group["hequity"] > 0) & group["equityfin"].notna()
    equityfin_data = group["equityfin"][mask]
    equityfin_weights = weights[mask]
    stats_equityfin = (
        DescrStatsW(equityfin_data, weights=equityfin_weights)
        if not equityfin_data.empty
        else None
    )

    return pd.DataFrame(
        {
            "age_lbl": [year],
            "race_lbl": [race_lbl],
            "fin": [
                (
                    stats_fin.quantile(0.5, return_pandas=False)[0]
                    if stats_fin
                    else np.nan
                ),
            ],
            "hequity": [
                (
                    stats_hequity.quantile(0.5, return_pandas=False)[0]
                    if stats_hequity
                    else np.nan
                ),
            ],
            "equityfin": [
                (
                    stats_equityfin.quantile(0.5, return_pandas=False)[0]
                    if stats_equityfin
                    else np.nan
                ),
            ],
        },
    )
