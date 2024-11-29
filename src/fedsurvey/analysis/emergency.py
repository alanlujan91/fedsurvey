"""Analyze emergency savings behavior."""

from __future__ import annotations

import pandas as pd

from ..exceptions import ProcessingError


def analyze_emergency_preparedness(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze emergency financial preparedness.

    Based on questions added in 2016 about how households would handle
    a hypothetical $400 emergency expense.

    Args:
    ----
        df: DataFrame containing SCF data with emergency response variables

    Returns:
    -------
        DataFrame with emergency response indicators

    Raises:
    ------
        ProcessingError: If required columns are missing
    """
    try:
        df = df.copy()

        # Validate required columns
        required_cols = ["X7775", "X7776", "X7777"]
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ProcessingError(f"Missing required columns: {missing_cols}")

        # How would handle $400 emergency expense
        response_map = {
            1: "borrow",
            2: "spend_savings",
            3: "postpone_payments",
            4: "cut_spending",
            5: "work_more",
        }
        df["emergency_response"] = df["X7775"].map(response_map)

        # Specific borrowing sources
        # Use parentheses and & for pandas boolean operations
        df["would_borrow_family"] = (df["X7776"].isin([1, 2])) | (
            df["X7777"].isin([1, 2])
        )
        df["would_borrow_credit"] = (df["X7776"] == 3) | (df["X7777"] == 3)
        df["would_borrow_bank"] = (df["X7776"].isin([10, 11])) | (
            df["X7777"].isin([10, 11])
        )
        df["would_borrow_alternative"] = (df["X7776"].between(4, 9)) | (
            df["X7777"].between(4, 9)
        )

        return df

    except KeyError as e:
        raise ProcessingError(f"Missing required column: {e}")
    except Exception as e:
        raise ProcessingError(f"Error analyzing emergency preparedness: {e}")
