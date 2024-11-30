"""Tests for data cleaning and harmonization."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from fedsurvey.scf.clean import adjust_for_inflation, apply_weights, harmonize_variables


@pytest.fixture
def sample_raw_data() -> pd.DataFrame:
    """Create sample raw SCF data for testing."""
    np.random.seed(42)
    n_samples = 100

    return pd.DataFrame(
        {
            "B3201": np.random.lognormal(10, 1, n_samples),  # Income
            "NETWORTH": np.random.lognormal(12, 2, n_samples),
            "X8022": np.random.randint(20, 90, n_samples, dtype=np.int64),  # Age
            "X5901": np.random.randint(1, 7, n_samples),  # Education
            "X6809": np.random.randint(1, 5, n_samples),  # Race
            "X8023": np.random.randint(1, 3, n_samples),  # Sex
            "X7372": np.random.randint(1, 3, n_samples),  # Marital status
            "year": np.repeat(1989, n_samples),
            "wgt": np.random.uniform(0.5, 1.5, n_samples),
        },
    )


def test_harmonize_variables(sample_raw_data: pd.DataFrame) -> None:
    """Test variable harmonization."""
    result = harmonize_variables(sample_raw_data, 1989)

    # Check required columns exist
    required_cols = [
        "income",
        "networth",
        "age",
        "education_label",
        "race_label",
        "marital_status",
        "year",
    ]
    assert all(col in result.columns for col in required_cols)

    # Check categorical variables are properly encoded
    assert all(isinstance(val, str) for val in result["education_label"])
    assert all(isinstance(val, str) for val in result["race_label"])

    # Check numeric variables
    assert result["income"].dtype in (np.float64, np.int64)
    assert result["networth"].dtype in (np.float64, np.int64)
    assert result["age"].dtype in (np.float64, np.int64, np.int32)


def test_adjust_for_inflation() -> None:
    """Test inflation adjustment."""
    df = pd.DataFrame(
        {
            "income": [50000, 75000, 100000],
            "networth": [250000, 500000, 1000000],
            "year": [1989, 1989, 1989],
        },
    )

    result = adjust_for_inflation(df)

    assert "income_adjusted" in result.columns
    assert "networth_adjusted" in result.columns

    # Check inflation adjustment factors using actual CPI ratio
    factor = 4376 / 1898  # 2022/1989 CPI ratio from bulletin.macro
    assert np.allclose(result["income_adjusted"], df["income"] * factor)
    assert np.allclose(result["networth_adjusted"], df["networth"] * factor)


def test_apply_weights() -> None:
    """Test weight application."""
    df = pd.DataFrame(
        {
            "income": [50000, 75000, 100000],
            "networth": [250000, 500000, 1000000],
            "wgt": [1.2, 0.8, 1.0],
        },
    )

    result = apply_weights(df)

    assert "income_weighted" in result.columns
    assert "networth_weighted" in result.columns

    # Check weighted values
    assert np.allclose(result["income_weighted"], df["income"] * df["wgt"])


def test_harmonize_variables_missing_data(sample_raw_data: pd.DataFrame) -> None:
    """Test harmonization with missing data."""
    sample_raw_data.loc[0, "X5901"] = np.nan

    result = harmonize_variables(sample_raw_data, 1989)

    assert pd.isna(result.loc[0, "education_label"])
    assert not pd.isna(result.loc[1:, "education_label"]).any()


def test_harmonize_variables_invalid_year() -> None:
    """Test harmonization with invalid year."""
    df = pd.DataFrame({"year": [1900]})

    with pytest.raises(ValueError, match="Invalid year"):
        harmonize_variables(df, 1900)


def test_adjust_for_inflation_future_year() -> None:
    """Test inflation adjustment with future year."""
    df = pd.DataFrame({"income": [50000], "year": [2025]})

    with pytest.raises(ValueError, match="No inflation data"):
        adjust_for_inflation(df)
