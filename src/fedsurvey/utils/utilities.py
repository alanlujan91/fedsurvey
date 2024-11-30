from __future__ import annotations

import warnings

warnings.simplefilter(action="ignore", category=FutureWarning)

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.ticker import FuncFormatter
from statsmodels.stats.weightstats import DescrStatsW


# Define a function for thousands formatting
def thousands_formater(x, pos) -> str:
    return "%1.1f" % (x / 1_000)


thousands_formater = FuncFormatter(thousands_formater)


def tens_of_thousands_formater(x, pos) -> str:
    return "%1.1f" % (x / 10_000)


tens_of_thousands_formater = FuncFormatter(tens_of_thousands_formater)


def hundreds_of_thousands_formater(x, pos) -> str:
    return "%1.1f" % (x / 100_000)


hundreds_of_thousands_formater = FuncFormatter(hundreds_of_thousands_formater)


def millions_formater(x, pos) -> str:
    return "%1.1f" % (x / 1_000_000)


millions_formater = FuncFormatter(millions_formater)


def billions_formater(x, pos) -> str:
    return "%1.1f" % (x / 1_000_000_000)


billions_formater = FuncFormatter(billions_formater)


def trillions_formater(x, pos) -> str:
    return "%1.1f" % (x / 1_000_000_000_000)


trillions_formater = FuncFormatter(trillions_formater)


def wmedian_lineplot(data, x, y, weights, style, errorbar=False):
    def compute_stats(group):
        stats = DescrStatsW(group[y], weights=group[weights])
        return pd.DataFrame(
            {
                x: group[x].iloc[0],
                style: group[style].iloc[0],
                "quantile_25": stats.quantile(0.25, return_pandas=False),
                "quantile_50": stats.quantile(0.5, return_pandas=False),
                "quantile_75": stats.quantile(0.75, return_pandas=False),
            },
        )

    temp_df = data.groupby([x, style]).apply(compute_stats)

    lineplot = sns.lineplot(
        data=temp_df,
        x=x,
        y="quantile_50",
        hue=style,
        style=style,
    )

    # Add fill_between for each style category
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

    # formatter = FuncFormatter(thousands_format)

    # # Check if maximum y value is greater than 1000 before applying the formatter
    # if temp_df["quantile_50"].max() > 1000:
    #     lineplot.yaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)  # Rotate x labels by 45 degrees

    return lineplot


def wmean_lineplot(data, x, y, weights, style, errorbar=False):
    def compute_stats(group):
        stats = DescrStatsW(group[y], weights=group[weights])

        return {
            x: group[x].iloc[0],
            style: group[style].iloc[0],
            "weighted_y": stats.mean,
            "weighted_std": stats.std,
        }

    temp_df = data.groupby([x, style]).apply(compute_stats).reset_index(drop=True)
    temp_df = pd.DataFrame(temp_df.tolist())

    lineplot = sns.lineplot(
        data=temp_df,
        x=x,
        y="weighted_y",
        hue=style,
        style=style,
    )

    # Add fill_between for each style category
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

    formatter = FuncFormatter(thousands_formater)

    # Check if maximum y value is greater than 1000 before applying the formatter
    if temp_df["weighted_y"].max() > 1000:
        lineplot.yaxis.set_major_formatter(formatter)

    plt.xticks(rotation=45)  # Rotate x labels by 45 degrees

    return lineplot


def weighted_relplot(data, x, y, weights, col, style):
    temp_df = data.groupby([x, col, style]).agg(
        weighted_y=pd.NamedAgg(
            column=y,
            aggfunc=lambda x: np.dot(x, data.loc[x.index, weights])
            / data.loc[x.index, weights].sum(),
        ),
    )

    relplot = sns.relplot(
        data=temp_df.reset_index(),
        x=x,
        y="weighted_y",
        hue=style,
        style=style,
        col=col,
        col_wrap=2,
        kind="line",
        markers="o",
        facet_kws={"sharey": False},  # Set sharey to False here
    )

    formatter = FuncFormatter(thousands_formater)

    # Rotate x labels by 45 degrees for all subplots
    for ax in relplot.axes.flatten():
        plt.setp(ax.get_xticklabels(), rotation=45)

        # Check if maximum y value is greater than 1000 before applying the formatter
        if max(ax.get_yticks()) > 1000:
            ax.yaxis.set_major_formatter(formatter)

    return relplot


def compute_means(group):
    year = group["age_lbl"].iloc[0]
    race_lbl = group["race_lbl"].iloc[0]
    weights = group["wgt"]

    stats_fin = DescrStatsW(group["fin"], weights=weights)
    stats_hequity = DescrStatsW(group["hequity"], weights=weights)
    mask = group["hequity"] > 0
    stats_equityfin = DescrStatsW(group["equityfin"][mask], weights=weights[mask])

    return pd.DataFrame(
        {
            "age_lbl": [year],
            "race_lbl": [race_lbl],
            "fin": [stats_fin.mean],
            "hequity": [stats_hequity.mean],
            "equityfin": [stats_equityfin.mean],
        },
    )


def compute_medians(group):
    year = group["age_lbl"].iloc[0]
    race_lbl = group["race_lbl"].iloc[0]
    weights = group["wgt"]

    stats_fin = DescrStatsW(group["fin"], weights=weights)
    stats_hequity = DescrStatsW(group["hequity"], weights=weights)
    mask = group["hequity"] > 0
    stats_equityfin = DescrStatsW(group["equityfin"][mask], weights=weights[mask])

    return pd.DataFrame(
        {
            "age_lbl": [year],
            "race_lbl": [race_lbl],
            "fin": stats_fin.quantile(0.5, return_pandas=False),
            "hequity": stats_hequity.mean,
            "equityfin": stats_equityfin.quantile(0.5, return_pandas=False),
        },
    )
