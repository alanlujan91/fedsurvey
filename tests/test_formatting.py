"""Tests for number formatting utilities."""

from __future__ import annotations

from fedsurvey.utils.formatting import (
    billions_formatter,
    millions_formatter,
    thousands_formatter,
    trillions_formatter,
)
from matplotlib.ticker import FuncFormatter


def test_thousands_formatter() -> None:
    """Test thousands formatting."""
    value = 1234567
    formatted = thousands_formatter(value, None)
    assert formatted == "1234.6"  # 1234.6 thousand


def test_millions_formatter() -> None:
    """Test millions formatting."""
    value = 1234567890
    formatted = millions_formatter(value, None)
    assert formatted == "1234.6"  # 1234.6 million


def test_billions_formatter() -> None:
    """Test billions formatting."""
    value = 1234567890000
    formatted = billions_formatter(value, None)
    assert formatted == "1234.6"  # 1234.6 billion


def test_trillions_formatter() -> None:
    """Test trillions formatting."""
    value = 1234567890000000
    formatted = trillions_formatter(value, None)
    assert formatted == "1234.6"  # 1234.6 trillion


def test_formatter_types() -> None:
    """Test formatter types."""
    assert isinstance(thousands_formatter, FuncFormatter)
    assert isinstance(millions_formatter, FuncFormatter)
    assert isinstance(billions_formatter, FuncFormatter)
    assert isinstance(trillions_formatter, FuncFormatter)
