"""Tests for financial literacy analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.literacy import calculate_finlit_score
from fedsurvey.exceptions import ProcessingError


@pytest.fixture()
def sample_literacy_data():
    """Create sample financial literacy data."""
    np.random.seed(42)
    n = 1000
    return pd.DataFrame(
        {
            "X7558": np.random.choice([1, 2, 3, 4, 5], n),  # Interest rate
            "X7559": np.random.choice([1, 2], n),  # Inflation
            "X7560": np.random.choice([1, 2, 3, 4, 5], n),  # Risk
            "X7556": np.random.randint(1, 11, n),  # Self-assessment
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_finlit_score_calculation(sample_literacy_data) -> None:
    """Test financial literacy score calculation."""
    result = calculate_finlit_score(sample_literacy_data)

    assert isinstance(result, pd.DataFrame)
    assert "finlit_score" in result.columns
    assert result["finlit_score"].between(0, 3).all()


def test_question_scoring(sample_literacy_data) -> None:
    """Test individual question scoring."""
    result = calculate_finlit_score(sample_literacy_data)

    question_cols = ["q1_correct", "q2_correct", "q3_correct"]
    assert all(col in result.columns for col in question_cols)
    # Check each column contains only 0s and 1s
    for col in question_cols:
        assert result[col].isin([0, 1]).all()


def test_self_assessment(sample_literacy_data) -> None:
    """Test self-assessment score."""
    result = calculate_finlit_score(sample_literacy_data)

    assert "finlit_self" in result.columns
    assert result["finlit_self"].between(1, 10).all()


def test_invalid_data() -> None:
    """Test handling of invalid data."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        calculate_finlit_score(invalid_df)
