"""Harmonize SCF variables across survey years."""

from __future__ import annotations

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
        ProcessingError: If year is invalid or required columns missing
    """
    try:
        # Validate year first
        if year < 1989 or year > 2022:
            raise ProcessingError(
                f"Invalid survey year: {year}. Must be between 1989 and 2022"
            )

        # Map raw SCF variables to standardized names based on bulletin.macro
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

        # Check required columns exist
        missing_cols = [col for col in VARIABLE_MAP.keys() if col not in df.columns]
        if missing_cols:
            raise ProcessingError(f"Missing required columns: {missing_cols}")

        df = df.copy()
        df = df.rename(columns=VARIABLE_MAP)

        # Add categorical labels
        df["education_label"] = df["education"].map(EDUCATION_MAP)
        df["race_label"] = df["race"].map(RACE_MAP)

        return df

    except ProcessingError as e:
        raise e
    except Exception as e:
        raise ProcessingError(f"Error harmonizing variables: {e}")
