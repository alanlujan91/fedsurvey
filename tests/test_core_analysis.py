"""Tests for core analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from fedsurvey.analyze.core import calculate_concentration, calculate_percentiles
from fedsurvey.core.exceptions import ProcessingError


@pytest.fixture
def sample_analysis_data():
    """Create sample data for analysis testing."""
    np.random.seed(42)
    n = 1000
    return pd.DataFrame(
        {
            "wealth": np.random.lognormal(10, 2, n),
            "income": np.random.lognormal(8, 1, n),
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_percentile_calculation(sample_analysis_data) -> None:
    """Test percentile calculations."""
    result = calculate_percentiles(sample_analysis_data, "wealth", "wgt", [10, 50, 90])

    assert isinstance(result, dict)
    assert all(0 <= p <= 100 for p in result)
    assert result[10] < result[50] < result[90]


def test_concentration_metrics(sample_analysis_data) -> None:
    """Test concentration metric calculations."""
    result = calculate_concentration(sample_analysis_data, "wealth", "wgt", [0.01, 0.1])

    assert isinstance(result, dict)
    assert all(0 <= share <= 1 for share in result.values())
    assert result["top_10"] > result["top_1"]
    assert result["top_1"] > 0.1
    assert result["top_10"] > 0.4


def test_invalid_inputs() -> None:
    """Test handling of invalid inputs."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        calculate_percentiles(invalid_df, "wealth")

    with pytest.raises(ProcessingError):
        calculate_concentration(invalid_df, "wealth")
