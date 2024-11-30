"""Analyze financial literacy based on SCF questions."""

from __future__ import annotations

from typing import TYPE_CHECKING

from fedsurvey.core.exceptions import ProcessingError

if TYPE_CHECKING:
    import pandas as pd


def calculate_finlit_score(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate financial literacy score from SCF questions.

    Based on questions added in 2016:
    - X7558: Interest rate question
    - X7559: Inflation question
    - X7560: Risk diversification question
    - X7556: Self-assessment (1-10 scale)

    Args:
    ----
        df: DataFrame containing SCF data with literacy questions

    Returns:
    -------
        DataFrame with literacy scores and question results

    Raises:
    ------
        ProcessingError: If required columns are missing

    """
    try:
        # Validate required columns
        required_cols = ["X7558", "X7559", "X7560", "X7556"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            msg = f"Missing required columns: {missing_cols}"
            raise ProcessingError(msg)

        df = df.copy()

        # Score each question (1 point per correct answer)
        # Interest rate question (correct = 5)
        df["q1_correct"] = (df["X7558"] == 5).astype(int)

        # Inflation question (correct = 1)
        df["q2_correct"] = (df["X7559"] == 1).astype(int)

        # Risk diversification question (correct = 5)
        df["q3_correct"] = (df["X7560"] == 5).astype(int)

        # Total score (0-3)
        df["finlit_score"] = df[["q1_correct", "q2_correct", "q3_correct"]].sum(axis=1)

        # Knowledge self-assessment (1-10 scale)
        df["finlit_self"] = df["X7556"]

        return df

    except KeyError as e:
        msg = f"Missing required column: {e}"
        raise ProcessingError(msg)
    except Exception as e:
        msg = f"Error calculating financial literacy score: {e}"
        raise ProcessingError(msg)
