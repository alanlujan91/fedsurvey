"""Analyze business ownership and characteristics."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def analyze_business_ownership(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze business ownership patterns and characteristics."""
    df = df.copy()

    # Active vs passive business ownership
    df["has_active_business"] = df["actbus"] > 0
    df["has_passive_business"] = df["nonactbus"] > 0
    df["has_any_business"] = df["hbus"] == 1

    # Business value components
    df["business_equity"] = df["bus"]
    df["business_income"] = df["bussefarminc"]

    # Business debt indicators
    df["has_business_collateral"] = (
        (df["X3121"].isin([1, 6]))
        | (df["X3221"].isin([1, 6]))
        | (df["X3321"].isin([1, 6]))
    )

    return df


def categorize_business_type(df: pd.DataFrame) -> pd.DataFrame:
    """Categorize businesses by type and management."""
    df = df.copy()

    # Management type
    df["self_employed"] = df["X4106"].isin([2, 3, 4])
    df["partnership"] = df["X3119"] == 2
    df["sole_prop"] = df["X3119"] == 1
    df["corporation"] = df["X3119"].isin([3, 4])

    return df
