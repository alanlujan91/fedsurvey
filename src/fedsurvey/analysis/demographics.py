"""Module for analyzing wealth distribution across demographic groups."""

from __future__ import annotations

import pandas as pd

from fedsurvey.exceptions import ProcessingError
from fedsurvey.utils.stats import weighted_mean, weighted_quantile


def wealth_by_education(
    df: pd.DataFrame,
    measures: list[str] | None = None,
    weight_col: str = "wgt",
    normalize: bool = True,
) -> pd.DataFrame:
    """Analyze wealth distribution by education level.

    Args:
    ----
        df: DataFrame containing SCF data
        measures: List of wealth/income measures to analyze
        weight_col: Name of survey weight column
        normalize: Whether to normalize by overall mean

    Returns:
    -------
        DataFrame with wealth statistics by education level

    Raises:
    ------
        ProcessingError: If DataFrame is empty or missing required columns

    """
    if measures is None:
        measures = ["networth", "financial_assets", "income"]
    try:
        # Check for empty DataFrame first
        if df.empty:
            msg = "Empty DataFrame provided"
            raise ProcessingError(msg)

        # Validate required columns
        required_cols = [*measures, "education_label", weight_col]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            msg = f"Missing required columns: {missing_cols}"
            raise ProcessingError(msg)

        stats = []
        for measure in measures:
            grouped = df.groupby("education_label", observed=True)
            weighted_means = grouped[measure].apply(
                lambda x: weighted_mean(x, df.loc[x.index, weight_col]),
            )

            if normalize:
                weighted_means = weighted_means / weighted_means.mean()

            stats.append(weighted_means)

        return pd.DataFrame(stats, index=measures)
    except Exception as e:
        msg = f"Error analyzing wealth by education: {e}"
        raise ProcessingError(msg)


def racial_wealth_gap(
    df: pd.DataFrame,
    base_group: str = "White non-Hispanic",
    measures: list[str] | None = None,
    weight_col: str = "wgt",
    by_year: bool = True,
) -> pd.DataFrame:
    """Analyze racial wealth disparities over time.

    Args:
    ----
        df: DataFrame containing SCF data
        base_group: Reference group for comparisons
        measures: List of measures to analyze
        weight_col: Name of weight column
        by_year: Whether to calculate by year

    Returns:
    -------
        DataFrame with wealth gaps relative to base group

    """
    if measures is None:
        measures = ["networth", "income"]
    try:
        df = df.copy()
        if by_year:
            # Reset index to avoid groupby issues
            df = df.reset_index(drop=True)
            # Use observed=True and include_groups=False to handle deprecation
            return df.groupby("year", observed=True).apply(
                lambda x: _calculate_gaps(x, base_group, measures, weight_col),
                include_groups=False,
            )
        return _calculate_gaps(df, base_group, measures, weight_col)
    except Exception as e:
        msg = f"Error analyzing racial wealth gap: {e}"
        raise ProcessingError(msg)


def _calculate_gaps(
    df: pd.DataFrame,
    base_group: str,
    measures: list[str],
    weight_col: str,
) -> pd.DataFrame:
    """Helper function to calculate wealth gaps."""
    gaps = pd.DataFrame()

    for measure in measures:
        base = df[df["race_label"] == base_group]
        if len(base) == 0:
            msg = f"Base group '{base_group}' not found in data"
            raise ValueError(msg)

        base_median = weighted_quantile(base[measure], base[weight_col], 0.5)

        for group in df["race_label"].unique():
            if group != base_group:
                group_data = df[df["race_label"] == group]
                if len(group_data) > 0:
                    group_median = weighted_quantile(
                        group_data[measure],
                        group_data[weight_col],
                        0.5,
                    )
                    gaps.loc[group, measure] = group_median / base_median

    return gaps


def intersectional_wealth_gap(
    df: pd.DataFrame,
    primary_group: str = "race_label",
    secondary_group: str = "education_label",
    base_groups: tuple = ("White non-Hispanic", "College grad"),
    measures: list[str] | None = None,
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Analyze wealth gaps across intersecting demographic characteristics.

    Args:
    ----
        df: DataFrame containing SCF data
        primary_group: Primary grouping variable
        secondary_group: Secondary grouping variable
        base_groups: Reference groups for comparison
        measures: List of measures to analyze
        weight_col: Name of weight column

    Returns:
    -------
        DataFrame with intersectional wealth gaps

    """
    if measures is None:
        measures = ["networth", "income"]
    try:
        df = df.copy()
        gaps = pd.DataFrame()

        base_data = df[
            (df[primary_group] == base_groups[0])
            & (df[secondary_group] == base_groups[1])
        ]
        if len(base_data) == 0:
            msg = f"Base groups {base_groups} not found in data"
            raise ValueError(msg)

        for measure in measures:
            base_median = weighted_quantile(
                base_data[measure],
                base_data[weight_col],
                0.5,
            )

            for p_group in df[primary_group].unique():
                for s_group in df[secondary_group].unique():
                    group_data = df[
                        (df[primary_group] == p_group)
                        & (df[secondary_group] == s_group)
                    ]
                    if len(group_data) > 0:
                        group_median = weighted_quantile(
                            group_data[measure],
                            group_data[weight_col],
                            0.5,
                        )
                        gaps.loc[f"{p_group}-{s_group}", measure] = (
                            group_median / base_median
                        )

        return gaps
    except Exception as e:
        msg = f"Error analyzing intersectional gaps: {e}"
        raise ProcessingError(msg)
