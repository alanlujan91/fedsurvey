"""Clean and harmonize SCF data."""

from __future__ import annotations

from typing import List, Optional

import pandas as pd

from ..exceptions import ProcessingError


def harmonize_variables(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Harmonize variable names and codes across survey years.

    Args:
    ----
        df: DataFrame containing SCF data
        year: Survey year

    Returns:
    -------
        DataFrame with harmonized variables

    Raises:
    ------
        ValueError: If year is invalid

    """
    if year < 1989 or year > 2022:
        raise ValueError(f"Invalid year: {year}. Must be between 1989 and 2022")

    # Map raw SCF variables to standardized names
    VARIABLE_MAP = {
        "B3201": "income",
        "NETWORTH": "networth",
        "X8022": "age",
        "X5901": "education",
        "X6809": "race",
        "X8023": "sex",
        "X7372": "marital_status",
    }

    # Education codes from bulletin.macro
    EDUCATION_MAP = {
        1: "Less than HS",
        2: "Some HS",
        3: "HS grad",
        4: "Some college",
        5: "College grad",
        6: "Graduate degree",
    }

    # Race codes from bulletin.macro
    RACE_MAP = {
        1: "White non-Hispanic",
        2: "Black",
        3: "Hispanic",
        4: "Asian",
        5: "Other/Multiple race",
    }

    try:
        df = df.copy()
        df = df.rename(columns=VARIABLE_MAP)
        df["education_label"] = df["education"].map(EDUCATION_MAP)
        df["race_label"] = df["race"].map(RACE_MAP)
        return df

    except Exception as e:
        raise ProcessingError(f"Error harmonizing variables: {e}")


def adjust_for_inflation(
    df: pd.DataFrame,
    monetary_cols: Optional[List[str]] = None,
    base_year: int = 2022,
) -> pd.DataFrame:
    """Adjust monetary values for inflation using CPI-U-RS.

    Args:
    ----
        df: DataFrame containing SCF data
        monetary_cols: List of columns to adjust
        base_year: Year to adjust values to

    Returns:
    -------
        DataFrame with inflation-adjusted values

    Raises:
    ------
        ValueError: If year is not in CPI data

    """
    # CPI-U-RS values from bulletin.macro
    CPI_DATA = {
        1989: 1898,
        1992: 2112,
        1995: 2261,
        1998: 2400,
        2001: 2614,
        2004: 2785,
        2007: 3058,
        2010: 3204,
        2013: 3438,
        2016: 3548,
        2019: 3775,
        2022: 4376,
    }

    try:
        if base_year not in CPI_DATA:
            raise ValueError(f"No inflation data available for year {base_year}")

        if monetary_cols is None:
            monetary_cols = ["income", "networth"]

        df = df.copy()
        for year in df["year"].unique():
            if year not in CPI_DATA:
                raise ValueError(f"No inflation data available for year {year}")

            factor = CPI_DATA[base_year] / CPI_DATA[year]
            mask = df["year"] == year
            for col in monetary_cols:
                if col in df.columns:
                    df.loc[mask, f"{col}_adjusted"] = df.loc[mask, col] * factor

        return df

    except ValueError as e:
        # Re-raise ValueError directly for expected validation errors
        raise e
    except Exception as e:
        raise ProcessingError(f"Error adjusting for inflation: {e}")


def apply_weights(
    df: pd.DataFrame,
    weight_col: str = "wgt",
    value_cols: Optional[List[str]] = None,
) -> pd.DataFrame:
    """Apply survey weights to monetary values.

    Args:
    ----
        df: DataFrame containing SCF data
        weight_col: Name of weight column
        value_cols: List of columns to weight

    Returns:
    -------
        DataFrame with weighted values

    """
    try:
        if value_cols is None:
            value_cols = ["income", "networth"]

        df = df.copy()
        for col in value_cols:
            if col in df.columns:
                df[f"{col}_weighted"] = df[col] * df[weight_col]
        return df

    except Exception as e:
        raise ProcessingError(f"Error applying weights: {e}")
