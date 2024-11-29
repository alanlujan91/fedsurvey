"""Harmonize race/ethnicity variables following Fed methodology."""

from __future__ import annotations

import pandas as pd

from ..exceptions import ProcessingError


def harmonize_race(df: pd.DataFrame, year: int) -> pd.DataFrame:
    """Harmonize race/ethnicity variables across survey years.

    Based on Moore & Pence (2021) "Improving the Measurement of Racial
    Disparities in the Survey of Consumer Finances"

    Args:
    ----
        df: DataFrame containing SCF data
        year: Survey year

    Returns:
    -------
        DataFrame with harmonized race/ethnicity categories

    Raises:
    ------
        ProcessingError: If year is invalid or required columns missing

    """
    try:
        if year < 1989 or year > 2022:
            raise ProcessingError(f"Invalid survey year: {year}")

        df = df.copy()
        df["race_4cat"] = pd.NA

        if year >= 2004:
            # Post-2004 uses Hispanic origin question
            # Hispanic takes precedence
            df.loc[df["X7004"] == 1, "race_4cat"] = "Hispanic"

            # Then assign race for non-Hispanics
            non_hispanic = df["X7004"] == 0
            df.loc[non_hispanic & (df["X6809"] == 1), "race_4cat"] = (
                "White non-Hispanic"
            )
            df.loc[non_hispanic & (df["X6809"] == 2), "race_4cat"] = "Black"
            df.loc[non_hispanic & (df["X6809"] == 4), "race_4cat"] = "Asian"
            df.loc[non_hispanic & df["race_4cat"].isna(), "race_4cat"] = (
                "Other/Multiple race"
            )

        else:
            # Pre-2004 uses single race question
            race_map = {
                1: "White non-Hispanic",
                2: "Black",
                3: "Hispanic",
                4: "Asian",
                5: "Other/Multiple race",
            }
            df["race_4cat"] = df["X6809"].map(race_map)

        return df

    except Exception as e:
        raise ProcessingError(f"Error harmonizing race variables: {e}")
