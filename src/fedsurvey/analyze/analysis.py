"""Module for statistical analysis of SCF data."""

from __future__ import annotations

import numpy as np
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
    if weights is None:
        return {p: df[variable].quantile(p / 100) for p in percentiles}

    return {
        p: weighted_quantile(df[variable], df[weights], p / 100) for p in percentiles
    }


def gini_coefficient(values: np.ndarray, weights: np.ndarray | None = None) -> float:
    """Calculate the Gini coefficient of inequality."""
    if weights is None:
        weights = np.ones_like(values)

    sorted_indices = np.argsort(values)
    values = values[sorted_indices]
    weights = weights[sorted_indices]

    cumw = np.cumsum(weights)
    cumval = np.cumsum(values * weights)

    return (np.sum(cumval * weights) / (cumval[-1] * cumw[-1])) - (
        cumw * weights
    ).sum() / (cumw[-1] * weights.sum())


def wealth_shares(
    df: pd.DataFrame,
    wealth_col: str = "networth",
    weight_col: str = "wgt",
    groups: list[float] | None = None,
) -> dict[str, float]:
    """Calculate wealth shares for different percentile groups."""
    if groups is None:
        groups = [0.5, 0.9, 0.99]
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


def calculate_age_wealth_profile(
    df: pd.DataFrame,
    wealth_col: str = "networth",
    weight_col: str = "wgt",
    age_bins: list[int] | None = None,
) -> pd.DataFrame:
    """Calculate median wealth by age group."""
    if age_bins is None:
        age_bins = [25, 35, 45, 55, 65, 75, 85]
    df["age_group"] = pd.cut(df["age"], bins=age_bins)

    profiles = []
    for year in df["year"].unique():
        year_data = df[df["year"] == year]
        medians = []
        for age_group in year_data["age_group"].unique():
            group_data = year_data[year_data["age_group"] == age_group]
            median = weighted_quantile(
                group_data[wealth_col],
                group_data[weight_col],
                0.5,
            )
            medians.append(
                {"year": year, "age_group": age_group, "median_wealth": median},
            )
        profiles.extend(medians)

    return pd.DataFrame(profiles)


def calculate_wealth_mobility(
    df: pd.DataFrame,
    base_year: int,
    target_year: int,
    wealth_col: str = "networth",
    weight_col: str = "wgt",
    quintiles: bool = True,
) -> pd.DataFrame:
    """Calculate wealth mobility between two survey years."""
    base = df[df["year"] == base_year]
    target = df[df["year"] == target_year]

    # Calculate wealth percentiles
    n_groups = 5 if quintiles else 10
    base["wealth_group"] = pd.qcut(
        base[wealth_col],
        q=n_groups,
        labels=[f"Q{i+1}" for i in range(n_groups)],
    )
    target["wealth_group"] = pd.qcut(
        target[wealth_col],
        q=n_groups,
        labels=[f"Q{i+1}" for i in range(n_groups)],
    )

    # Create transition matrix
    return pd.crosstab(
        base["wealth_group"],
        target["wealth_group"],
        base[weight_col],
        normalize="index",
    )


def decompose_inequality(
    df: pd.DataFrame,
    components: list[str],
    weight_col: str = "wgt",
) -> dict[str, float]:
    """Decompose wealth inequality into components."""
    total_wealth = df["networth"]
    total_gini = gini_coefficient(total_wealth, df[weight_col])

    # Calculate component shares and correlations
    results = {}
    for component in components:
        share = (df[component] * df[weight_col]).sum() / (
            total_wealth * df[weight_col]
        ).sum()
        component_gini = gini_coefficient(df[component], df[weight_col])
        correlation = np.corrcoef(total_wealth, df[component])[0, 1]

        contribution = share * component_gini * correlation
        results[component] = {
            "share": share,
            "gini": component_gini,
            "correlation": correlation,
            "contribution": contribution,
            "relative_contribution": contribution / total_gini,
        }

    return results
