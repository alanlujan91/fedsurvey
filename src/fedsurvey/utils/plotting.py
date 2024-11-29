"""Utilities for plotting."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from statsmodels.stats.weightstats import DescrStatsW


def wmedian_lineplot(data, x, y, weights, style, errorbar=False):
    """Create weighted median line plot.

    Args:
    ----
        data: DataFrame containing plot data
        x: Column name for x-axis
        y: Column name for y-axis
        weights: Column name for weights
        style: Column name for line styles
        errorbar: Whether to show error bars

    Returns:
    -------
        Matplotlib axes object
    """

    def compute_stats(group):
        stats = DescrStatsW(group[y], weights=group[weights])
        return pd.DataFrame(
            {
                "quantile_25": [stats.quantile(0.25, return_pandas=False)[0]],
                "quantile_50": [stats.quantile(0.5, return_pandas=False)[0]],
                "quantile_75": [stats.quantile(0.75, return_pandas=False)[0]],
            },
        )

    # Group and compute stats, excluding grouping columns
    temp_df = (
        data.groupby([x, style], observed=True)
        .apply(compute_stats, include_groups=False)
        .reset_index()
    )

    # Create line plot
    lineplot = sns.lineplot(
        data=temp_df,
        x=x,
        y="quantile_50",
        hue=style,
        style=style,
        markers=True,
        dashes=False,
    )

    if errorbar:
        styles = temp_df[style].unique()
        for s in styles:
            df_style = temp_df[temp_df[style] == s]
            plt.fill_between(
                df_style[x],
                df_style["quantile_25"],
                df_style["quantile_75"],
                alpha=0.3,
            )

    plt.xticks(rotation=45)
    return lineplot


def wmean_lineplot(data, x, y, weights, style, errorbar=False):
    """Create weighted mean line plot."""

    def compute_stats(group):
        stats = DescrStatsW(group[y], weights=group[weights])
        return pd.DataFrame(
            {
                "weighted_y": [stats.mean],
                "weighted_std": [stats.std],
            },
        )

    # Group and compute stats, excluding grouping columns
    temp_df = (
        data.groupby([x, style], observed=True)
        .apply(compute_stats, include_groups=False)
        .reset_index()
    )

    # Create line plot
    lineplot = sns.lineplot(
        data=temp_df,
        x=x,
        y="weighted_y",
        hue=style,
        style=style,
        markers=True,
        dashes=False,
    )

    if errorbar:
        styles = temp_df[style].unique()
        for s in styles:
            df_style = temp_df[temp_df[style] == s]
            plt.fill_between(
                df_style[x],
                df_style["weighted_y"] + df_style["weighted_std"],
                df_style["weighted_y"] - df_style["weighted_std"],
                alpha=0.3,
            )

    plt.xticks(rotation=45)
    return lineplot


def weighted_relplot(data, x, y, weights, col, style):
    """Create weighted relational plot."""
    # Compute weighted means
    temp_df = (
        data.groupby([x, col, style], observed=True)
        .apply(
            lambda g: pd.Series(
                {
                    "weighted_y": np.average(g[y], weights=g[weights]),
                },
            ),
            include_groups=False,
        )
        .reset_index()
    )

    # Create relational plot with consistent markers
    relplot = sns.relplot(
        data=temp_df,
        x=x,
        y="weighted_y",
        hue=style,
        style=style,
        col=col,
        col_wrap=2,
        kind="line",
        markers=["o", "s"],  # Specify different markers for each style
        dashes=False,
        facet_kws={"sharey": False},
    )

    for ax in relplot.axes.flatten():
        plt.setp(ax.get_xticklabels(), rotation=45)

    return relplot
