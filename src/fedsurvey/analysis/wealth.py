"""Module for analyzing wealth distribution and composition.

This module provides tools for analyzing the composition and distribution of household wealth
using Survey of Consumer Finances (SCF) data. It includes functions for:

- Calculating wealth composition across different asset types
- Analyzing wealth-to-income ratios
- Computing intergenerational wealth differences
- Decomposing wealth inequality by components

Examples
--------
    >>> import pandas as pd
    >>> from fedsurvey.analysis.wealth import wealth_composition
    >>>
    >>> # Calculate wealth composition shares
    >>> shares = wealth_composition(df, components=['financial_assets', 'home_value'])
    >>> print(shares)
           financial_assets_share  home_value_share
    year
    2019               0.324159          0.675841

"""

from __future__ import annotations

import pandas as pd

from fedsurvey.exceptions import ProcessingError


def wealth_composition(
    df: pd.DataFrame,
    components: list[str] | None = None,
    by_group: str | None = None,
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Analyze composition of household wealth across different components."""
    if components is None:
        components = [
            "financial_assets",
            "business_value",
            "home_value",
            "retirement_accounts",
        ]
    try:
        # Validate empty DataFrame first
        if df.empty:
            msg = "Empty DataFrame provided"
            raise ProcessingError(msg)

        # Validate components exist in DataFrame
        missing_cols = [col for col in components if col not in df.columns]
        if missing_cols:
            msg = f"Missing required columns: {missing_cols}"
            raise ProcessingError(msg)

        if by_group and by_group not in df.columns:
            msg = f"Group column '{by_group}' not found"
            raise ProcessingError(msg)

        df = df.copy()
        shares = pd.DataFrame()

        def calculate_shares(data):
            total_wealth = (data["networth"] * data[weight_col]).sum()
            if total_wealth == 0:
                return pd.Series({f"{c}_share": 0 for c in components})

            shares = {}
            for component in components:
                shares[f"{component}_share"] = (
                    data[component] * data[weight_col]
                ).sum() / total_wealth
            return pd.Series(shares)

        if by_group:
            # Calculate shares by group
            shares = df.groupby(by_group).apply(calculate_shares)
        else:
            # Calculate overall shares
            shares = calculate_shares(df).to_frame().T

        return shares

    except Exception as e:
        msg = f"Error calculating wealth composition: {e}"
        raise ProcessingError(msg)


def detailed_wealth_composition(
    df: pd.DataFrame,
    components: list[str] | None = None,
    by_percentile: bool = True,
    n_percentiles: int = 5,
    weight_col: str = "wgt",
) -> pd.DataFrame:
    """Analyze detailed wealth composition across the wealth distribution.

    Shows how portfolio composition varies across wealth percentiles.
    Includes both broad categories and detailed components.

    Args:
    ----
        df: DataFrame containing SCF data
        components: List of wealth component columns
        by_percentile: Whether to break down by wealth percentiles
        n_percentiles: Number of percentile groups
        weight_col: Name of weight column

    Returns:
    -------
        DataFrame with detailed wealth composition shares

    Raises:
    ------
        ProcessingError: If required columns are missing

    """
    if components is None:
        components = [
            "fin",
            "nfin",
            "debt",
            "checking",
            "savings",
            "stocks",
            "bonds",
            "vehicles",
            "houses",
            "business",
            "credit_card",
            "mortgages",
            "education_loans",
        ]
    try:
        # Validate components exist in DataFrame
        missing_cols = [col for col in components if col not in df.columns]
        if missing_cols:
            msg = f"Missing required columns: {missing_cols}"
            raise ProcessingError(msg)

        df = df.copy()
        if by_percentile:
            df["wealth_percentile"] = pd.qcut(
                df["networth"],
                n_percentiles,
                labels=[f"P{i}" for i in range(n_percentiles)],
            )

        compositions = []
        for group in df["wealth_percentile"].unique():
            group_data = df[df["wealth_percentile"] == group]

            comp = {}
            total_wealth = (group_data["networth"] * group_data[weight_col]).sum()

            for component in components:
                comp[f"{component}_share"] = (
                    group_data[component] * group_data[weight_col]
                ).sum() / total_wealth

            compositions.append(comp)

        return pd.DataFrame(compositions)

    except KeyError as e:
        msg = f"Error accessing column: {e}"
        raise ProcessingError(msg)
    except Exception as e:
        msg = f"Error calculating detailed wealth composition: {e}"
        raise ProcessingError(msg)
