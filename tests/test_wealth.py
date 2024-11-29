"""Tests for wealth analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.wealth import detailed_wealth_composition, wealth_composition
from fedsurvey.exceptions import ProcessingError


@pytest.fixture()
def sample_wealth_data():
    """Create sample wealth data."""
    np.random.seed(42)
    n = 1000
    networth = np.random.lognormal(10, 2, n)

    return pd.DataFrame(
        {
            "networth": networth,
            "financial_assets": networth * 0.4,
            "business_value": networth * 0.2,
            "home_value": networth * 0.3,
            "retirement_accounts": networth * 0.1,
            "fin": networth * 0.4,
            "nfin": networth * 0.5,
            "debt": networth * 0.1,
            "checking": networth * 0.05,
            "savings": networth * 0.05,
            "stocks": networth * 0.1,
            "bonds": networth * 0.05,
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_wealth_composition(sample_wealth_data):
    """Test wealth composition analysis."""
    components = [
        "financial_assets",
        "business_value",
        "home_value",
        "retirement_accounts",
    ]

    result = wealth_composition(sample_wealth_data, components)

    assert isinstance(result, pd.DataFrame)
    assert all(col.endswith("_share") for col in result.columns)
    assert np.allclose(result.sum(axis=1), 1)  # Shares sum to 1


def test_detailed_composition(sample_wealth_data):
    """Test detailed wealth composition analysis."""
    components = ["fin", "nfin", "debt", "checking", "savings", "stocks", "bonds"]

    result = detailed_wealth_composition(
        sample_wealth_data,
        components,
        by_percentile=True,
        n_percentiles=5,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 5  # Five percentiles
    assert all(col.endswith("_share") for col in result.columns)


def test_invalid_components():
    """Test handling of invalid components."""
    df = pd.DataFrame({"networth": [100000], "wgt": [1]})

    with pytest.raises(ProcessingError):
        wealth_composition(df, ["invalid_component"])


def test_negative_values(sample_wealth_data):
    """Test handling of negative values."""
    sample_wealth_data.loc[0, "networth"] = -100000

    result = wealth_composition(sample_wealth_data)
    assert isinstance(result, pd.DataFrame)
