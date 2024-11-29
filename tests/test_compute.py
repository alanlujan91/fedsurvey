"""Tests for computation utilities."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.utils.compute import compute_means, compute_medians


@pytest.fixture()
def sample_compute_data():
    """Create sample data for computation tests."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame(
        {
            "age_lbl": np.repeat(["25-34", "35-44"], n // 2),
            "race_lbl": np.repeat(["White", "Black"], n // 2),
            "fin": np.random.lognormal(10, 1, n),
            "hequity": np.random.lognormal(9, 1, n),
            "equityfin": np.random.uniform(0, 1, n),
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_compute_means(sample_compute_data):
    """Test mean computation."""
    result = compute_means(sample_compute_data)

    assert isinstance(result, pd.DataFrame)
    assert all(col in result.columns for col in ["fin", "hequity", "equityfin"])
    assert len(result) == 1  # One row per group


def test_compute_medians(sample_compute_data):
    """Test median computation."""
    result = compute_medians(sample_compute_data)

    assert isinstance(result, pd.DataFrame)
    assert all(col in result.columns for col in ["fin", "hequity", "equityfin"])
    assert len(result) == 1


def test_compute_with_missing_data():
    """Test computation with missing data."""
    df = pd.DataFrame(
        {
            "age_lbl": ["25-34"],
            "race_lbl": ["White"],
            "fin": [np.nan],
            "hequity": [100000],
            "equityfin": [0.5],
            "wgt": [1.0],
        },
    )

    result_means = compute_means(df)
    result_medians = compute_medians(df)

    assert pd.isna(result_means["fin"].iloc[0])
    assert not pd.isna(result_means["hequity"].iloc[0])
