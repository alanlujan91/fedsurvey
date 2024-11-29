"""Analyze household debt payments and payment ratios."""

from __future__ import annotations

import pandas as pd


def calculate_payment_ratios(df: pd.DataFrame) -> pd.DataFrame:
    """Calculate payment-to-income ratios following Fed methodology.

    Calculates:
    - Total payment ratio
    - Mortgage payment ratio
    - Consumer debt payment ratio
    - Revolving debt payment ratio
    """
    df = df.copy()

    # Monthly income (with minimum floor of $100 as in bulletin)
    monthly_income = df["income"].clip(lower=100) / 12

    # Calculate ratios
    df["pir_total"] = df["tpay"] / monthly_income
    df["pir_mortgage"] = df["mortpay"] / monthly_income
    df["pir_consumer"] = df["conspay"] / monthly_income
    df["pir_revolving"] = df["revpay"] / monthly_income

    # Flag high payment burden (>40% of income)
    df["high_payment_burden"] = df["pir_total"] > 0.4

    return df


def analyze_payment_types(df: pd.DataFrame) -> pd.DataFrame:
    """Analyze types of payments and payment vehicles used."""
    df = df.copy()

    # Credit access indicators
    df["has_credit_card"] = ~df["noccbal"]  # Not no credit card balance
    df["has_heloc"] = df["heloc_yn"] == 1
    df["has_loc"] = df["othloc"] > 0

    # Payment difficulties
    df["payment_late"] = df["late"] == 1
    df["payment_60plus_late"] = df["late60"] == 1
    df["turned_down_credit"] = df["turndown"] == 1
    df["fear_denial"] = df["feardenial"] == 1

    return df
