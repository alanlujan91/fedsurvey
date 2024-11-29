"""Tests for inflation adjustment utilities."""

from __future__ import annotations

import pytest
from fedsurvey.utils.inflation import get_inflation_factor


def test_inflation_factors():
    """Test inflation factor calculations."""
    # 2022 base year factor from bulletin.macro
    assert get_inflation_factor(1989, 2022) == pytest.approx(4376 / 1898, rel=1e-3)
    assert get_inflation_factor(2019, 2022) == pytest.approx(4376 / 3775, rel=1e-3)


def test_invalid_years():
    """Test handling of invalid years."""
    with pytest.raises(ValueError):
        get_inflation_factor(1900, 2022)
