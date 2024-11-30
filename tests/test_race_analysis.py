"""Tests for race/ethnicity analysis."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from fedsurvey.core.exceptions import ProcessingError
from fedsurvey.scf.race import harmonize_race


@pytest.fixture
def sample_race_data():
    """Create sample race/ethnicity data."""
    np.random.seed(42)
    n = 1000

    # Pre-2004 data
    pre2004 = pd.DataFrame(
        {"X6809": np.random.choice([1, 2, 3, 4, 5], n // 2), "year": 1998},
    )

    # Post-2004 data
    post2004 = pd.DataFrame(
        {
            "X6809": np.random.choice([1, 2, 3, 4, 5], n // 2),
            "X7004": np.random.choice([0, 1], n // 2),  # Hispanic origin
            "year": 2019,
        },
    )

    return pd.concat([pre2004, post2004], ignore_index=True)


def test_pre2004_harmonization(sample_race_data) -> None:
    """Test pre-2004 race harmonization."""
    pre2004_data = sample_race_data[sample_race_data["year"] < 2004]
    result = harmonize_race(pre2004_data, 1998)

    assert isinstance(result, pd.DataFrame)
    assert "race_4cat" in result.columns
    assert all(
        result["race_4cat"].isin(
            ["White non-Hispanic", "Black", "Hispanic", "Asian", "Other/Multiple race"],
        ),
    )


def test_post2004_harmonization(sample_race_data) -> None:
    """Test post-2004 race harmonization."""
    post2004_data = sample_race_data[sample_race_data["year"] >= 2004]
    result = harmonize_race(post2004_data, 2019)

    assert isinstance(result, pd.DataFrame)
    assert "race_4cat" in result.columns
    # Hispanic origin should take precedence
    hispanic_mask = post2004_data["X7004"] == 1
    assert all(result.loc[hispanic_mask, "race_4cat"] == "Hispanic")


def test_invalid_year() -> None:
    """Test handling of invalid year."""
    df = pd.DataFrame({"X6809": [1], "year": 1900})

    with pytest.raises(ProcessingError):
        harmonize_race(df, 1900)
