"""Tests for trend analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.trends import (
    concentration_trends,
    mobility_analysis,
    wealth_growth_rates,
)
from fedsurvey.exceptions import ProcessingError


@pytest.fixture()
def sample_trend_data():
    """Create sample data for trend analysis."""
    np.random.seed(42)
    n = 1000
    years = [2019, 2022]
    data = []

    for year in years:
        networth = np.random.lognormal(10, 2, n)
        data.append(
            pd.DataFrame(
                {
                    "year": year,
                    "networth": networth,
                    "financial_assets": networth * 0.4,
                    "income": np.random.lognormal(8, 1, n),
                    "wgt": np.random.uniform(0.5, 1.5, n),
                },
            ),
        )

    return pd.concat(data, ignore_index=True)


def test_wealth_growth_rates(sample_trend_data) -> None:
    """Test wealth growth rate calculations."""
    result = wealth_growth_rates(
        sample_trend_data,
        measures=["networth", "income"],
        percentiles=[10, 50, 90],
    )

    assert isinstance(result, pd.DataFrame)
    # Growth rates for each year relative to previous
    assert len(result.dropna()) == 1  # One growth rate period (2022 relative to 2019)
    assert all(col.startswith(("networth", "income")) for col in result.columns)
    # Growth rates should be reasonable (between -50% and +100%)
    assert all(-0.5 <= x <= 1.0 for x in result.values.flatten() if not pd.isna(x))


def test_concentration_trends(sample_trend_data) -> None:
    """Test concentration trend analysis."""
    result = concentration_trends(
        sample_trend_data,
        measures=["networth", "financial_assets"],
        top_shares=[0.01, 0.1],
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two years
    assert all(0 <= val <= 1 for val in result.values.flatten())


def test_mobility_analysis(sample_trend_data) -> None:
    """Test mobility analysis."""
    result = mobility_analysis(
        sample_trend_data,
        base_year=2019,
        end_year=2022,
        n_quantiles=5,
    )

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (5, 5)  # 5x5 transition matrix
    # Each row should sum to 1 (if not empty)
    assert all(
        np.allclose(row.sum(), 1) if row.sum() > 0 else True
        for _, row in result.iterrows()
    )


def test_invalid_years() -> None:
    """Test handling of invalid years."""
    df = pd.DataFrame(
        {"year": [2019, 2019], "networth": [100000, 200000], "wgt": [1, 1]},
    )

    with pytest.raises(ProcessingError):
        mobility_analysis(df, 2019, 2020)


def test_insufficient_data() -> None:
    """Test handling of insufficient data."""
    df = pd.DataFrame({"year": [2019], "networth": [100000], "wgt": [1]})

    with pytest.raises(ProcessingError):
        wealth_growth_rates(df)
