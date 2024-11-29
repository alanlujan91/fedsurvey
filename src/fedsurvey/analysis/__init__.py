"""Analysis modules for SCF data."""

from __future__ import annotations

from ..utils.compute import compute_means, compute_medians
from ..utils.stats import (
    calculate_top_share,
    gini_coefficient,
    weighted_mean,
    weighted_quantile,
    weighted_std,
)
from .core import calculate_concentration, calculate_percentiles
from .demographics import (
    intersectional_wealth_gap,
    racial_wealth_gap,
    wealth_by_education,
)
from .trends import (
    concentration_trends,
    mobility_analysis,
    wealth_growth_rates,
    wealth_mobility,
)
from .wealth import detailed_wealth_composition, wealth_composition


def wealth_shares(
    df,
    wealth_col: str = "networth",
    weight_col: str = "wgt",
    groups: list[float] = [0.5, 0.9, 0.99],
) -> dict[str, float]:
    """Calculate wealth shares for different percentile groups."""
    total_wealth = (df[wealth_col] * df[weight_col]).sum()
    shares = {}

    for pct in groups:
        threshold = weighted_quantile(df[wealth_col], df[weight_col], pct)
        top_wealth = df[df[wealth_col] >= threshold][wealth_col]
        top_weights = df[df[wealth_col] >= threshold][weight_col]
        shares[f"top_{int(100*(1-pct))}"] = (
            top_wealth * top_weights
        ).sum() / total_wealth

    return shares


__all__ = [
    "calculate_percentiles",
    "calculate_concentration",
    "wealth_by_education",
    "racial_wealth_gap",
    "intersectional_wealth_gap",
    "wealth_growth_rates",
    "concentration_trends",
    "mobility_analysis",
    "wealth_mobility",
    "wealth_composition",
    "detailed_wealth_composition",
    "gini_coefficient",
    "weighted_mean",
    "weighted_quantile",
    "weighted_std",
    "compute_means",
    "compute_medians",
    "calculate_top_share",
    "wealth_shares",
]
