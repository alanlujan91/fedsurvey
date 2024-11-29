"""Tests for variable harmonization."""

from __future__ import annotations

import pandas as pd
import pytest
from fedsurvey.exceptions import ProcessingError
from fedsurvey.scf.harmonize import harmonize_variables


@pytest.fixture()
def raw_scf_data():
    """Create sample raw SCF data."""
    return pd.DataFrame(
        {
            "B3201": [50000, 75000],
            "NETWORTH": [250000, 500000],
            "X8022": [35, 45],
            "X5901": [3, 5],
            "X6809": [1, 2],
            "X8023": [1, 2],
            "X7372": [1, 2],
        },
    )


def test_variable_renaming(raw_scf_data) -> None:
    """Test variable renaming."""
    result = harmonize_variables(raw_scf_data, 2019)

    expected_cols = [
        "income",
        "networth",
        "age",
        "education",
        "race",
        "sex",
        "marital_status",
        "education_label",
        "race_label",
    ]
    assert all(col in result.columns for col in expected_cols)


def test_education_mapping(raw_scf_data) -> None:
    """Test education level mapping."""
    result = harmonize_variables(raw_scf_data, 2019)

    assert result["education_label"].iloc[0] == "HS grad"
    assert result["education_label"].iloc[1] == "College grad"


def test_invalid_year() -> None:
    """Test handling of invalid survey year."""
    df = pd.DataFrame({"B3201": [50000]})

    with pytest.raises(ProcessingError, match="Invalid survey year"):
        harmonize_variables(df, 1900)


def test_missing_columns() -> None:
    """Test handling of missing required columns."""
    df = pd.DataFrame({"other_col": [1, 2, 3]})

    with pytest.raises(ProcessingError, match="Missing required columns"):
        harmonize_variables(df, 2019)
