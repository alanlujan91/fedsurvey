"""Utilities for number formatting."""

from __future__ import annotations

from matplotlib.ticker import FuncFormatter


def thousands_formater(x, pos) -> str:
    """Format numbers in thousands."""
    return "%1.1f" % (x / 1_000)


def tens_of_thousands_formater(x, pos) -> str:
    """Format numbers in tens of thousands."""
    return "%1.1f" % (x / 10_000)


def hundreds_of_thousands_formater(x, pos) -> str:
    """Format numbers in hundreds of thousands."""
    return "%1.1f" % (x / 100_000)


def millions_formater(x, pos) -> str:
    """Format numbers in millions."""
    return "%1.1f" % (x / 1_000_000)


def billions_formater(x, pos) -> str:
    """Format numbers in billions."""
    return "%1.1f" % (x / 1_000_000_000)


def trillions_formater(x, pos) -> str:
    """Format numbers in trillions."""
    return "%1.1f" % (x / 1_000_000_000_000)


# Create formatter instances
thousands_formatter = FuncFormatter(thousands_formater)
tens_of_thousands_formatter = FuncFormatter(tens_of_thousands_formater)
hundreds_of_thousands_formatter = FuncFormatter(hundreds_of_thousands_formater)
millions_formatter = FuncFormatter(millions_formater)
billions_formatter = FuncFormatter(billions_formater)
trillions_formatter = FuncFormatter(trillions_formater)
