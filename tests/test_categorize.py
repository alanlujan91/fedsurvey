"""Tests for variable categorization."""

from __future__ import annotations

import pandas as pd
from fedsurvey.scf.categorize import categorize_income, categorize_work_status


def test_income_categories():
    """Test income categorization."""
    df = pd.DataFrame({"income": [5000, 15000, 30000, 75000, 150000]})

    result = categorize_income(df)
    assert list(result["income_cat"]) == [1, 2, 3, 4, 5]


def test_work_status():
    """Test work status categorization."""
    df = pd.DataFrame({"X4106": [1, 2, 50, 21], "age": [45, 50, 70, 70]})

    result = categorize_work_status(df)
    assert list(result["work_status"]) == [1, 2, 3, 3]
