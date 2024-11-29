"""Module for visualizing wealth distributions and trends."""

from __future__ import annotations

from typing import List, Optional, Tuple

import matplotlib

matplotlib.use("Agg")  # Use Agg backend to avoid Tcl/Tk issues

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from ..analysis.demographics import racial_wealth_gap
from ..analysis.trends import wealth_mobility
from ..analysis.wealth import (
    detailed_wealth_composition,
    wealth_composition,
)

# Set default style - use seaborn-v0_8-darkgrid for newer seaborn versions
plt.style.use("seaborn-v0_8-darkgrid")


def plot_wealth_distribution(
    df: pd.DataFrame,
    year: Optional[int] = None,
    log_scale: bool = True,
    weighted: bool = True,
    figsize: Optional[Tuple[int, int]] = None,
) -> plt.Figure:
    """Plot the distribution of wealth."""
    if df.empty:
        raise ValueError("Empty DataFrame provided")

    fig, ax = plt.subplots(figsize=figsize or (10, 6))

    data = df if year is None else df[df["year"] == year]
    wealth_col = "networth" if not weighted else "networth"

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
    if df.empty:
        raise ValueError("Empty DataFrame provided")

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


def plot_wealth_composition_trends(
    df: pd.DataFrame,
    components: List[str],
    by_group: Optional[str] = None,
    figsize: tuple[int, int] = (12, 6),
) -> plt.Figure:
    """Plot trends in wealth composition over time."""
    if df.empty:
        raise ValueError("Empty DataFrame provided")

    fig, ax = plt.subplots(figsize=figsize)

    composition = wealth_composition(df, components, by_group)
    composition.plot(kind="area", stacked=True, ax=ax)

    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total Wealth")
    ax.set_title("Wealth Composition Over Time")

    return fig


def plot_racial_wealth_gap(
    df: pd.DataFrame,
    measures: List[str] = ["networth"],
    base_group: str = "White non-Hispanic",
) -> plt.Figure:
    """Plot racial wealth gaps over time."""
    if df.empty:
        raise ValueError("Empty DataFrame provided")

    fig, ax = plt.subplots(figsize=(12, 6))

    # Reset index to avoid groupby issues
    df = df.reset_index(drop=True)
    gaps = racial_wealth_gap(df, base_group, measures)
    gaps.plot(marker="o", ax=ax)

    ax.axhline(y=1, color="k", linestyle="--", alpha=0.3)
    ax.set_xlabel("Year")
    ax.set_ylabel("Ratio to White Households")
    ax.set_title("Racial Wealth Gap Over Time")

    return fig


def plot_wealth_mobility_heatmap(
    df: pd.DataFrame,
    measure: str = "networth",
    n_quantiles: int = 5,
    cmap: str = "YlOrRd",
) -> plt.Figure:
    """Plot heatmap showing wealth mobility between quantiles."""
    if df.empty:
        raise ValueError("Empty DataFrame provided")

    # Reset index to avoid groupby issues
    df = df.reset_index(drop=True)
    mobility_data = wealth_mobility(df, n_quantiles=n_quantiles, measures=[measure])

    # Handle empty mobility data
    if mobility_data.empty:
        raise ValueError("No mobility data available")

    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(
        mobility_data.fillna(0),  # Fill NaN values with 0
        cmap=cmap,
        annot=True,
        fmt=".2f",
        ax=ax,
    )

    ax.set_title("Wealth Mobility Between Survey Years")
    return fig


def plot_wealth_composition_by_percentile(
    df: pd.DataFrame,
    components: List[str],
    n_percentiles: int = 5,
) -> plt.Figure:
    """Plot stacked bar chart of wealth composition by percentile."""
    if df.empty:
        raise ValueError("Empty DataFrame provided")

    composition = detailed_wealth_composition(
        df,
        components,
        by_percentile=True,
        n_percentiles=n_percentiles,
    )

    fig, ax = plt.subplots(figsize=(12, 6))
    composition.plot(kind="bar", stacked=True, ax=ax)

    ax.set_xlabel("Wealth Percentile")
    ax.set_ylabel("Share of Total Wealth")
    ax.set_title("Wealth Composition Across the Distribution")

    return fig
