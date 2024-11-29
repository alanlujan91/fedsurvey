"""Analysis of household income composition and dynamics."""

from __future__ import annotations

import pandas as pd

from fedsurvey.exceptions import ProcessingError


def analyze_income_sources(
    df: pd.DataFrame,
    weight_col: str = "wgt",
    by_year: bool = True,
    by_wealth_group: bool = False,
) -> pd.DataFrame:
    """Analyze income composition following bulletin methodology.

    Components from bulletin:
    1. Wages and salaries
    2. Business/farm/self-employment
    3. Interest and dividends
    4. Capital gains
    5. Social Security/retirement
    6. Transfer/other income
    """
    try:
        df = df.copy()  # Make copy to avoid SettingWithCopyWarning

        # Components from bulletin.macro
        components = {
            "wages": ["wageinc"],
            "business": ["bussefarminc"],
            "interest_div": ["intdivinc"],
            "capital_gains": ["kginc"],
            "retirement": ["ssretinc"],
            "transfers": ["transfothinc"],
        }

        def calc_shares(data: pd.DataFrame) -> pd.Series:
            """Calculate income shares for a group."""
            total_income = (data["income"] * data[weight_col]).sum()
            shares = {}

            for comp_name, comp_vars in components.items():
                comp_sum = data[comp_vars].sum(axis=1)
                shares[f"{comp_name}_share"] = (
                    comp_sum * data[weight_col]
                ).sum() / total_income

            return pd.Series(shares)

        # Calculate shares by group
        if by_year:
            result = df.groupby("year", observed=True).apply(
                calc_shares,
                include_groups=False,
            )

        if by_wealth_group:
            # Create wealth quintiles
            df["wealth_group"] = pd.qcut(
                df["networth"],
                q=5,
                labels=[f"Q{i+1}" for i in range(5)],
            )
            result = df.groupby(["year", "wealth_group"], observed=True).apply(
                calc_shares,
                include_groups=False,
            )

        return result

    except Exception as e:
        msg = f"Error analyzing income sources: {e}"
        raise ProcessingError(msg)


def analyze_income_mobility(
    df: pd.DataFrame,
    base_year: int,
    end_year: int,
    weight_col: str = "wgt",
    n_quantiles: int = 5,
) -> pd.DataFrame:
    """Analyze income mobility between survey waves.

    Creates transition matrix showing movement between income quantiles.

    Args:
    ----
        df: DataFrame containing SCF data
        base_year: Starting year
        end_year: Ending year
        weight_col: Name of weight column
        n_quantiles: Number of quantile groups

    Returns:
    -------
        DataFrame with transition probabilities

    """
    try:
        # Get data for both years
        base = df[df["year"] == base_year].copy()
        end = df[df["year"] == end_year].copy()

        if len(base) == 0 or len(end) == 0:
            msg = f"No data found for years {base_year} and/or {end_year}"
            raise ValueError(msg)

        # Create income quantiles
        base["income_group"] = pd.qcut(
            base["income"],
            q=n_quantiles,
            labels=[f"Q{i+1}" for i in range(n_quantiles)],
        )
        end["income_group"] = pd.qcut(
            end["income"],
            q=n_quantiles,
            labels=[f"Q{i+1}" for i in range(n_quantiles)],
        )

        # Create transition matrix with weighted counts
        transition = pd.crosstab(
            base["income_group"],
            end["income_group"],
            values=base[weight_col],
            aggfunc="sum",
            normalize="index",
        ).fillna(0)

        # Ensure all quantiles are represented
        all_labels = [f"Q{i+1}" for i in range(n_quantiles)]
        return transition.reindex(
            index=all_labels,
            columns=all_labels,
            fill_value=0,
        )

    except Exception as e:
        msg = f"Error analyzing income mobility: {e}"
        raise ProcessingError(msg)
