"""Tests for race/ethnicity harmonization."""

from __future__ import annotations

import pandas as pd
from fedsurvey.scf.race import harmonize_race


def test_post2004_race():
    """Test post-2004 race/ethnicity harmonization."""
    df = pd.DataFrame(
        {
            "X7004": [1, 0, 0, 0, 0],  # Hispanic origin
            "X6809": [1, 1, 2, 4, 5],  # Race
        },
    )

    result = harmonize_race(df, 2019)
    expected = [
        "Hispanic",
        "White non-Hispanic",
        "Black",
        "Asian",
        "Other/Multiple race",
    ]
    assert list(result["race_4cat"]) == expected


def test_pre2004_race():
    """Test pre-2004 race/ethnicity harmonization."""
    df = pd.DataFrame({"X6809": [1, 2, 3, 4, 5]})

    result = harmonize_race(df, 1998)
    expected = [
        "White non-Hispanic",
        "Black",
        "Hispanic",
        "Asian",
        "Other/Multiple race",
    ]
    assert list(result["race_4cat"]) == expected
