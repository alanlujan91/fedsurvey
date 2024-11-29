"""Utilities for inflation adjustment using CPI-U-RS."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd

CPI_U_RS = {
    # September values from bulletin.macro
    1989: 1898,
    1992: 2112,
    1995: 2261,
    1998: 2400,
    2001: 2614,
    2004: 2785,
    2007: 3058,
    2010: 3204,
    2013: 3438,
    2016: 3548,
    2019: 3775,
    2022: 4376,
}


def get_inflation_factor(
    from_year: int,
    to_year: int = 2022,
    cpi_data: dict[int, float] = CPI_U_RS,
) -> float:
    """Calculate inflation adjustment factor between years."""
    if from_year not in cpi_data or to_year not in cpi_data:
        msg = f"CPI data not available for {from_year} or {to_year}"
        raise ValueError(msg)
    return cpi_data[to_year] / cpi_data[from_year]


def adjust_for_inflation(
    df: pd.DataFrame,
    monetary_cols: list[str],
    base_year: int = 2022,
) -> pd.DataFrame:
    """Adjust monetary values for inflation to specified base year."""
    df = df.copy()

    for year in df["year"].unique():
        factor = get_inflation_factor(year, base_year)
        mask = df["year"] == year
        for col in monetary_cols:
            df.loc[mask, f"{col}_real"] = df.loc[mask, col] * factor

    return df
