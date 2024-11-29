"""Tests for business analysis."""

from __future__ import annotations

import pandas as pd
from fedsurvey.analysis.business import (
    analyze_business_ownership,
)


def test_business_ownership():
    """Test business ownership analysis."""
    df = pd.DataFrame(
        {
            "actbus": [10000, 0, 0],
            "nonactbus": [0, 5000, 0],
            "hbus": [1, 1, 0],
            "bus": [10000, 5000, 0],
            "bussefarminc": [5000, 1000, 0],
            "X3121": [1, 0, 0],
            "X3221": [0, 0, 0],
            "X3321": [0, 0, 0],
        },
    )

    result = analyze_business_ownership(df)

    assert list(result["has_active_business"]) == [True, False, False]
    assert list(result["has_passive_business"]) == [False, True, False]
    assert list(result["has_any_business"]) == [True, True, False]
