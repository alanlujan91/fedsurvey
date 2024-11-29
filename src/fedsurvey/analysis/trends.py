"""Module for analyzing wealth trends over time."""

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from ..exceptions import ProcessingError
from ..utils.stats import calculate_top_share, weighted_quantile


def wealth_growth_rates(
    df: pd.DataFrame,
    measures: List[str] = ["networth", "income"],
    percentiles: List[float] = [10, 50, 90],
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Calculate growth rates of wealth measures over time.

    Args:
    ----
        df: DataFrame containing SCF data
        measures: List of measures to analyze
        percentiles: List of percentiles to calculate
        weight_col: Name of weight column

    Returns:
    -------
        DataFrame with growth rates by year

    """
    try:
        growth = pd.DataFrame()

        for measure in measures:
            # Calculate percentiles by year
            yearly_stats = []
            for p in percentiles:
                stats = df.groupby("year", observed=True)[measure].apply(
                    lambda x: weighted_quantile(
                        x,
                        df.loc[x.index, weight_col],
                        p / 100,
                    ),
                    include_groups=False,
                )
                yearly_stats.append((p, stats))

            # Calculate growth rates
            for p, stats in yearly_stats:
                growth[f"{measure}_p{int(p)}"] = stats.pct_change()

        return growth

    except Exception as e:
        raise ProcessingError(f"Error calculating growth rates: {e}")


def concentration_trends(
    df: pd.DataFrame,
    measures: List[str] = ["networth", "financial_assets"],
    top_shares: List[float] = [0.01, 0.1, 0.5],
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Analyze trends in wealth concentration over time."""
    try:
        trends = pd.DataFrame()

        for measure in measures:
            for share in top_shares:
                # Calculate shares by year
                yearly_shares = df.groupby("year", observed=True).apply(
                    lambda x: calculate_top_share(
                        x[measure],
                        x[weight_col],
                        share,
                    ),
                    include_groups=False,
                )
                trends[f"{measure}_top{int(share*100)}"] = yearly_shares

        return trends

    except Exception as e:
        raise ProcessingError(f"Error calculating concentration trends: {e}")


def wealth_mobility(
    df: pd.DataFrame,
    n_quantiles: int = 5,
    measures: List[str] = ["networth"],
    weight_col: str = "wgt",
    by_group: Optional[str] = None,
) -> pd.DataFrame:
    """Analyze movement between wealth quantiles across survey years."""
    try:
        if df.empty:
            raise ProcessingError("Empty DataFrame provided")

        df = df.copy()

        # Validate required columns
        if by_group and by_group not in df.columns:
            raise ProcessingError(f"Group column '{by_group}' not found")

        # Create transition matrix for each year pair
        years = sorted(df["year"].unique())
        if len(years) < 2:
            raise ProcessingError("Need at least two years of data")

        transitions = []
        for i in range(len(years) - 1):
            year1, year2 = years[i], years[i + 1]

            # Get data for each year and create new DataFrames to avoid SettingWithCopyWarning
            base = df[df["year"] == year1].copy()
            end = df[df["year"] == year2].copy()

            # Create quantiles within each year
            base.loc[:, "quantile"] = pd.qcut(
                base[measures[0]],
                n_quantiles,
                labels=False,
            )
            end.loc[:, "quantile"] = pd.qcut(
                end[measures[0]],
                n_quantiles,
                labels=False,
            )

            # Create transition matrix
            matrix = pd.crosstab(
                base["quantile"],
                end["quantile"],
                values=base[weight_col],
                aggfunc="sum",
                normalize="index",
            ).fillna(0)

            # Reshape to 1D array and add to transitions
            transitions.append(matrix.values.flatten())

        # Create DataFrame with transitions
        mobility = pd.DataFrame(
            transitions,
            columns=[
                f"Q{i+1}_to_Q{j+1}"
                for i in range(n_quantiles)
                for j in range(n_quantiles)
            ],
            index=[f"{years[i]}-{years[i+1]}" for i in range(len(years) - 1)],
        )

        return mobility

    except Exception as e:
        raise ProcessingError(f"Error analyzing mobility: {e}")


def mobility_analysis(
    df: pd.DataFrame,
    base_year: int,
    end_year: int,
    n_quantiles: int = 5,
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Analyze movement between wealth quantiles across survey years.

    Args:
    ----
        df: DataFrame containing SCF data
        base_year: Starting year
        end_year: Ending year
        n_quantiles: Number of quantile groups
        weight_col: Name of weight column

    Returns:
    -------
        DataFrame with transition probabilities

    Raises:
    ------
        ProcessingError: If years not found or insufficient data

    """
    try:
        # Get data for both years
        base = df[df["year"] == base_year].copy()
        end = df[df["year"] == end_year].copy()

        if len(base) == 0 or len(end) == 0:
            raise ProcessingError(
                f"No data found for years {base_year} and/or {end_year}",
            )

        # Create wealth quantiles
        base["wealth_quantile"] = pd.qcut(
            base["networth"],
            q=n_quantiles,
            labels=False,
        )
        end["wealth_quantile"] = pd.qcut(
            end["networth"],
            q=n_quantiles,
            labels=False,
        )

        # Create transition matrix with weighted counts
        transition = pd.crosstab(
            base["wealth_quantile"],
            end["wealth_quantile"],
            values=base[weight_col],
            aggfunc="sum",
            normalize="index",
        ).fillna(0)

        # Ensure all quantiles are represented
        all_labels = range(n_quantiles)
        transition = transition.reindex(
            index=all_labels,
            columns=all_labels,
            fill_value=0,
        )

        return transition

    except Exception as e:
        raise ProcessingError(f"Error analyzing mobility: {e}")
