"""Module for visualizing SCF data."""

from __future__ import annotations

from typing import List, Optional

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def plot_wealth_distribution(
    df: pd.DataFrame,
    year: Optional[int] = None,
    log_scale: bool = True,
    weighted: bool = True,
) -> plt.Figure:
    """Plot the distribution of wealth."""
    fig, ax = plt.subplots(figsize=(10, 6))

    data = df if year is None else df[df["year"] == year]
    wealth_col = "networth_weighted" if weighted else "networth"

    if log_scale:
        data = data[data[wealth_col] > 0]
        sns.histplot(data=data, x=wealth_col, log_scale=True, ax=ax)
        ax.set_xlabel("Wealth (log scale)")
    else:
        sns.histplot(data=data, x=wealth_col, ax=ax)
        ax.set_xlabel("Wealth")

    ax.set_title(f"Wealth Distribution {year if year else 'All Years'}")
    return fig


def plot_lorenz_curve(
    df: pd.DataFrame,
    wealth_col: str = "networth",
    weight_col: str = "wgt",
    year: Optional[int] = None,
) -> plt.Figure:
    """Plot Lorenz curve for wealth distribution."""
    fig, ax = plt.subplots(figsize=(8, 8))

    data = df if year is None else df[df["year"] == year]

    # Calculate Lorenz curve
    sorted_idx = data[wealth_col].argsort()
    cum_wealth = (
        data[wealth_col].iloc[sorted_idx] * data[weight_col].iloc[sorted_idx]
    ).cumsum()
    cum_pop = data[weight_col].iloc[sorted_idx].cumsum()

    # Normalize to percentages
    cum_wealth = cum_wealth / cum_wealth.iloc[-1]
    cum_pop = cum_pop / cum_pop.iloc[-1]

    # Plot
    ax.plot(cum_pop, cum_wealth, label="Lorenz Curve")
    ax.plot([0, 1], [0, 1], "--", label="Line of Perfect Equality")

    ax.set_xlabel("Cumulative Share of Population")
    ax.set_ylabel("Cumulative Share of Wealth")
    ax.set_title(f"Lorenz Curve {year if year else 'All Years'}")
    ax.legend()

    return fig


def plot_age_wealth_profile(
    df: pd.DataFrame,
    years: Optional[List[int]] = None,
    log_scale: bool = True,
    adjust_inflation: bool = True,
) -> plt.Figure:
    """Plot wealth profiles by age group across survey years."""
    fig, ax = plt.subplots(figsize=(12, 8))

    data = calculate_age_wealth_profile(df)
    if years:
        data = data[data["year"].isin(years)]

    for year in sorted(data["year"].unique()):
        year_data = data[data["year"] == year]
        ax.plot(
            year_data["age_group"].astype(str),
            year_data["median_wealth"],
            marker="o",
            label=str(year),
        )

    if log_scale:
        ax.set_yscale("log")

    ax.set_xlabel("Age Group")
    ax.set_ylabel("Median Wealth" + (" (log scale)" if log_scale else ""))
    ax.legend(title="Survey Year")
    ax.grid(True, alpha=0.3)

    return fig


def plot_wealth_components(
    df: pd.DataFrame,
    components: List[str],
    year: Optional[int] = None,
    stacked: bool = True,
) -> plt.Figure:
    """Plot composition of household wealth."""
    fig, ax = plt.subplots(figsize=(12, 6))

    data = df if year is None else df[df["year"] == year]

    if stacked:
        data[components].plot(kind="area", stacked=True, ax=ax)
    else:
        data[components].plot(kind="bar", ax=ax)

    ax.set_xlabel("Household")
    ax.set_ylabel("Value")
    ax.legend(title="Components")

    return fig
