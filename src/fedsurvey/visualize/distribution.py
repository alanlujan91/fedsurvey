"""Module for visualizing wealth distributions and trends."""

from __future__ import annotations

from typing import TYPE_CHECKING

import matplotlib as mpl

mpl.use("Agg")  # Use Agg backend to avoid Tcl/Tk issues

import matplotlib.pyplot as plt
import seaborn as sns

from fedsurvey.analyze.demographics import racial_wealth_gap
from fedsurvey.analyze.trends import wealth_mobility
from fedsurvey.analyze.wealth import detailed_wealth_composition, wealth_composition

if TYPE_CHECKING:
    import pandas as pd

# Set default style - use seaborn-v0_8-darkgrid for newer seaborn versions
plt.style.use("seaborn-v0_8-darkgrid")


def plot_wealth_distribution(
    df: pd.DataFrame,
    year: int | None = None,
    log_scale: bool = True,
    weighted: bool = True,
    figsize: tuple[int, int] | None = None,
) -> plt.Figure:
    """Plot the distribution of wealth."""
    if df.empty:
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

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
    year: int | None = None,
) -> plt.Figure:
    """Plot Lorenz curve for wealth distribution."""
    if df.empty:
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

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
    components: list[str],
    by_group: str | None = None,
    figsize: tuple[int, int] = (12, 6),
) -> plt.Figure:
    """Plot trends in wealth composition over time."""
    if df.empty:
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

    fig, ax = plt.subplots(figsize=figsize)

    composition = wealth_composition(df, components, by_group)
    composition.plot(kind="area", stacked=True, ax=ax)

    ax.set_xlabel("Year")
    ax.set_ylabel("Share of Total Wealth")
    ax.set_title("Wealth Composition Over Time")

    return fig


def plot_racial_wealth_gap(
    df: pd.DataFrame,
    measures: list[str] | None = None,
    base_group: str = "White non-Hispanic",
) -> plt.Figure:
    """Plot racial wealth gaps over time."""
    if measures is None:
        measures = ["networth"]
    if df.empty:
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

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
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

    # Reset index to avoid groupby issues
    df = df.reset_index(drop=True)
    mobility_data = wealth_mobility(df, n_quantiles=n_quantiles, measures=[measure])

    # Handle empty mobility data
    if mobility_data.empty:
        msg = "No mobility data available"
        raise ValueError(msg)

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
    components: list[str],
    n_percentiles: int = 5,
) -> plt.Figure:
    """Plot stacked bar chart of wealth composition by percentile."""
    if df.empty:
        msg = "Empty DataFrame provided"
        raise ValueError(msg)

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
