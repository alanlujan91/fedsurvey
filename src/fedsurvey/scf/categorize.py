"""Categorize SCF variables based on bulletin definitions."""

from __future__ import annotations

import numpy as np
import pandas as pd

from fedsurvey.exceptions import ProcessingError


def categorize_income(
    df: pd.DataFrame,
    income_col: str = "income",
    bins: list[float] | None = None,
) -> pd.DataFrame:
    """Create income categories matching bulletin definitions.

    Args:
    ----
        df: DataFrame containing SCF data
        income_col: Name of income column
        bins: Custom bin edges (default from bulletin)

    Returns:
    -------
        DataFrame with income categories added

    """
    try:
        df = df.copy()

        if bins is None:
            bins = [0, 10000, 25000, 50000, 100000, float("inf")]

        labels = list(range(1, len(bins)))
        df["income_cat"] = pd.cut(df[income_col], bins=bins, labels=labels, right=False)
        return df
    except Exception as e:
        msg = f"Error categorizing income: {e}"
        raise ProcessingError(msg)


def categorize_work_status(
    df: pd.DataFrame,
    work_col: str = "X4106",
    age_col: str = "age",
) -> pd.DataFrame:
    """Create work status categories matching bulletin definitions.

    Categories:
    1 = work for someone else
    2 = self-employed/partnership
    3 = retired/disabled + (student/homemaker/misc not working and age 65+)
    4 = other groups not working (mainly under 65 and out of labor force)

    Args:
    ----
        df: DataFrame containing SCF data
        work_col: Name of work status column
        age_col: Name of age column

    Returns:
    -------
        DataFrame with work status categories added

    """
    try:
        df = df.copy()

        conditions = [
            df[work_col] == 1,
            df[work_col].isin([2, 3, 4]),
            (
                (df[work_col].isin([50, 52]))
                | (
                    df[work_col].isin([21, 23, 30, 70, 80, 97, 85])
                    & (df[age_col] >= 65)
                )
            ),
            df[age_col] < 65,
        ]
        choices = [1, 2, 3, 4]

        df["work_status"] = np.select(conditions, choices, default=np.nan)
        return df
    except Exception as e:
        msg = f"Error categorizing work status: {e}"
        raise ProcessingError(msg)
