"""Tests for emergency savings analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.emergency import analyze_emergency_preparedness
from fedsurvey.exceptions import ProcessingError


@pytest.fixture()
def sample_emergency_data():
    """Create sample emergency savings data."""
    np.random.seed(42)
    n = 1000
    return pd.DataFrame(
        {
            "X7775": np.random.choice([1, 2, 3, 4, 5], n),  # Emergency response
            "X7776": np.random.choice([1, 2, 3, 4, 5, 10, 11], n),  # First source
            "X7777": np.random.choice([1, 2, 3, 4, 5, 10, 11], n),  # Second source
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_emergency_response_analysis(sample_emergency_data):
    """Test emergency response analysis."""
    result = analyze_emergency_preparedness(sample_emergency_data)

    assert isinstance(result, pd.DataFrame)
    assert "emergency_response" in result.columns
    assert all(
        result["emergency_response"].isin(
            [
                "borrow",
                "spend_savings",
                "postpone_payments",
                "cut_spending",
                "work_more",
            ],
        ),
    )


def test_borrowing_sources(sample_emergency_data):
    """Test borrowing source analysis."""
    result = analyze_emergency_preparedness(sample_emergency_data)

    borrowing_cols = [
        "would_borrow_family",
        "would_borrow_credit",
        "would_borrow_bank",
        "would_borrow_alternative",
    ]
    assert all(col in result.columns for col in borrowing_cols)
    assert all(result[col].dtype == bool for col in borrowing_cols)


def test_invalid_data():
    """Test handling of invalid data."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        analyze_emergency_preparedness(invalid_df)
