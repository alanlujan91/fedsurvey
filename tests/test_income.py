"""Tests for income analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis.income import analyze_income_mobility, analyze_income_sources
from fedsurvey.exceptions import ProcessingError


@pytest.fixture()
def sample_income_data():
    """Create sample income data for testing."""
    np.random.seed(42)
    n = 1000

    # Generate correlated data for both years
    base_income = np.random.lognormal(8, 1, n // 2)
    end_income = base_income * np.random.lognormal(
        0,
        0.5,
        n // 2,
    )  # Some mobility but correlated

    data = []
    for year, income in [(2019, base_income), (2022, end_income)]:
        data.append(
            pd.DataFrame(
                {
                    "year": year,
                    "income": income,
                    "wageinc": income * 0.6,
                    "bussefarminc": income * 0.1,
                    "intdivinc": income * 0.05,
                    "kginc": income * 0.05,
                    "ssretinc": income * 0.15,
                    "transfothinc": income * 0.05,
                    "networth": np.random.lognormal(10, 2, n // 2),
                    "wgt": np.random.uniform(0.5, 1.5, n // 2),
                },
            ),
        )

    return pd.concat(data, ignore_index=True)


def test_income_sources_by_year(sample_income_data) -> None:
    """Test income source analysis by year."""
    result = analyze_income_sources(sample_income_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two years
    assert all(0 <= val <= 1 for val in result.values.flatten())
    assert all(col.endswith("_share") for col in result.columns)


def test_income_sources_by_wealth_group(sample_income_data) -> None:
    """Test income source analysis by wealth group."""
    result = analyze_income_sources(
        sample_income_data,
        by_year=False,
        by_wealth_group=True,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 10  # 2 years * 5 wealth quintiles
    assert all(0 <= val <= 1 for val in result.values.flatten())


def test_income_mobility(sample_income_data) -> None:
    """Test income mobility analysis."""
    result = analyze_income_mobility(
        sample_income_data,
        base_year=2019,
        end_year=2022,
        n_quantiles=5,
    )

    assert isinstance(result, pd.DataFrame)
    assert result.shape == (5, 5)  # 5x5 transition matrix
    # Each row should sum to 1 (if not empty)
    assert all(
        np.allclose(row.sum(), 1) if not np.allclose(row.sum(), 0) else True
        for _, row in result.iterrows()
    )


def test_invalid_years_mobility() -> None:
    """Test handling of invalid years in mobility analysis."""
    df = pd.DataFrame({"year": [2019, 2019], "income": [50000, 75000], "wgt": [1, 1]})

    with pytest.raises(ProcessingError):
        analyze_income_mobility(df, 2019, 2020)


def test_missing_columns() -> None:
    """Test handling of missing required columns."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        analyze_income_sources(invalid_df)
