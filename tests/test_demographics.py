"""Tests for demographic analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.demographics import (
    intersectional_wealth_gap,
    racial_wealth_gap,
    wealth_by_education,
)


@pytest.fixture()
def sample_data():
    """Create sample demographic data for testing."""
    np.random.seed(42)
    n = 1000

    return pd.DataFrame(
        {
            "networth": np.random.lognormal(10, 2, n),
            "income": np.random.lognormal(8, 1, n),
            "financial_assets": np.random.lognormal(8, 2, n),
            "education_label": np.random.choice(
                ["Less than HS", "HS grad", "College grad"],
                n,
                p=[0.2, 0.5, 0.3],
            ),
            "race_label": np.random.choice(
                ["White non-Hispanic", "Black", "Hispanic"],
                n,
                p=[0.6, 0.2, 0.2],
            ),
            "wgt": np.random.uniform(0.5, 1.5, n),
            "year": np.repeat([2019, 2022], n // 2),
        },
    )


def test_wealth_by_education(sample_data):
    """Test education wealth gap analysis."""
    result = wealth_by_education(sample_data)

    assert isinstance(result, pd.DataFrame)
    assert all(
        col in result.columns for col in ["Less than HS", "HS grad", "College grad"]
    )
    assert all(
        measure in result.index
        for measure in ["networth", "financial_assets", "income"]
    )
    assert np.allclose(result.mean(axis=1), 1.0, rtol=1e-10)  # Test normalization


def test_racial_wealth_gap(sample_data):
    """Test racial wealth gap analysis."""
    result = racial_wealth_gap(sample_data, by_year=True)

    assert isinstance(result, pd.DataFrame)
    assert len(result.index.levels[0]) == len(sample_data["year"].unique())
    assert all(
        group in result.index.get_level_values(1) for group in ["Black", "Hispanic"]
    )
    assert all(result.values.flatten() > 0)


def test_intersectional_wealth_gap(sample_data):
    """Test intersectional wealth gap analysis."""
    result = intersectional_wealth_gap(sample_data)

    assert isinstance(result, pd.DataFrame)
    expected_combinations = len(sample_data["race_label"].unique()) * len(
        sample_data["education_label"].unique(),
    )
    assert len(result) <= expected_combinations
    assert all("-" in idx for idx in result.index)  # Check for combined group labels
