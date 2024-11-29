"""Utilities for income adjustments."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pandas as pd


def adjust_lagged_income(
    df: pd.DataFrame,
    income_col: str = "income",
    year_col: str = "year",
) -> pd.DataFrame:
    """Adjust lagged income to survey year dollars using CPI factors."""
    # CPI factors for lagged income (from bulletin.macro)
    LAG_FACTORS = {
        1989: 1883 / 1805,
        1992: 2099 / 2048,
        1995: 2250 / 2197,
        1998: 2392 / 2360,
        2001: 2597 / 2525,
        2004: 2770 / 2698,
        2007: 3043 / 2950,
        2010: 3183 / 3105,
        2013: 3425 / 3355,
        2016: 3533 / 3475,
        2019: 3758 / 3675,
        2022: 4350 / 4075,
    }

    df = df.copy()
    df[f"{income_col}_adj"] = df.apply(
        lambda x: x[income_col] * LAG_FACTORS.get(x[year_col], 1),
        axis=1,
    )
    return df
