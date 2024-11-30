"""Tests for portfolio composition analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from fedsurvey.analyze.portfolio import (
    analyze_debt_composition,
    analyze_portfolio_composition,
)
from fedsurvey.core.exceptions import ProcessingError


@pytest.fixture
def sample_portfolio_data():
    """Create sample portfolio data for testing."""
    np.random.seed(42)
    n = 1000

    # Generate correlated portfolio components
    networth = np.random.lognormal(10, 2, n)
    return pd.DataFrame(
        {
            "year": np.repeat([2019, 2022], n // 2),
            "fin": networth * 0.7,
            "checking": networth * 0.1,
            "savings": networth * 0.1,
            "mmda": networth * 0.05,
            "call": networth * 0.05,
            "cds": networth * 0.05,
            "savbnd": networth * 0.05,
            "notxbnd": networth * 0.02,
            "mortbnd": networth * 0.02,
            "govtbnd": networth * 0.02,
            "obnd": networth * 0.02,
            "stocks": networth * 0.1,
            "stmutf": networth * 0.02,
            "tfbmutf": networth * 0.02,
            "gbmutf": networth * 0.02,
            "obmutf": networth * 0.02,
            "comutf": networth * 0.02,
            "retqliq": networth * 0.1,
            "cashli": networth * 0.05,
            "othma": networth * 0.02,
            "othfin": networth * 0.01,
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


@pytest.fixture
def sample_debt_data():
    """Create sample debt data for testing."""
    np.random.seed(42)
    n = 1000

    income = np.random.lognormal(8, 1, n)
    debt = np.random.lognormal(9, 2, n)
    return pd.DataFrame(
        {
            "year": np.repeat([2019, 2022], n // 2),
            "income": income,
            "debt": debt,
            "nh_mort": debt * 0.6,
            "resdbt": debt * 0.1,
            "ccbal": debt * 0.05,
            "veh_inst": debt * 0.1,
            "edn_inst": debt * 0.05,
            "othloc": debt * 0.05,
            "oth_inst": debt * 0.05,
            "paymortgages": income * 0.3 / 12,  # Monthly payments
            "paycredit_card": income * 0.05 / 12,
            "wgt": np.random.uniform(0.5, 1.5, n),
        },
    )


def test_portfolio_composition_by_year(sample_portfolio_data) -> None:
    """Test portfolio composition analysis by year."""
    result = analyze_portfolio_composition(sample_portfolio_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two years
    assert all(0 <= val <= 1 for val in result.values.flatten())
    assert all(col.endswith("_share") for col in result.columns)


def test_portfolio_composition_by_percentile(sample_portfolio_data) -> None:
    """Test portfolio composition analysis by wealth percentile."""
    result = analyze_portfolio_composition(
        sample_portfolio_data,
        by_year=False,
        by_percentile=True,
        n_percentiles=5,
    )

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 5  # Five percentiles
    assert all(0 <= val <= 1 for val in result.values.flatten())


def test_debt_composition_analysis(sample_debt_data) -> None:
    """Test debt composition analysis."""
    result = analyze_debt_composition(sample_debt_data)

    assert isinstance(result, pd.DataFrame)
    assert len(result) == 2  # Two years
    assert all(0 <= val <= 1 for val in result.values.flatten())
    assert "mortgages_pir" in result.columns
    assert "credit_card_pir" in result.columns


def test_invalid_data_handling() -> None:
    """Test handling of invalid data."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        analyze_portfolio_composition(invalid_df)

    with pytest.raises(ProcessingError):
        analyze_debt_composition(invalid_df)
