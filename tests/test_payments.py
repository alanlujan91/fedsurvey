"""Tests for payment analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
from fedsurvey.analysis.payments import analyze_payment_types, calculate_payment_ratios


def test_payment_ratios():
    """Test payment ratio calculations."""
    df = pd.DataFrame(
        {
            "income": [50000, 75000, 25000],
            "tpay": [1000, 1500, 800],
            "mortpay": [800, 1200, 0],
            "conspay": [200, 300, 500],
            "revpay": [0, 0, 300],
        },
    )

    result = calculate_payment_ratios(df)

    # Check total payment ratio calculation
    expected_pir = [0.24, 0.24, 0.384]  # (payment*12)/income
    assert np.allclose(result["pir_total"], expected_pir, rtol=1e-3)

    # Check high burden flag
    assert not result["high_payment_burden"].any()


def test_payment_types():
    """Test payment type analysis."""
    df = pd.DataFrame(
        {
            "noccbal": [True, False, True],
            "heloc_yn": [1, 0, 0],
            "othloc": [1000, 0, 0],
            "late": [1, 0, 0],
            "late60": [0, 0, 1],
            "turndown": [0, 1, 0],
            "feardenial": [1, 0, 0],
        },
    )

    result = analyze_payment_types(df)

    assert list(result["has_credit_card"]) == [False, True, False]
    assert list(result["has_heloc"]) == [True, False, False]
