"""Module for fetching related economic data from FRED."""

from __future__ import annotations

import pandas as pd
from fredapi import Fred

from ..core.config import FRED_API_KEY


class FREDData:
    """Class for fetching and managing FRED economic data."""

    def __init__(self, api_key: str | None = None) -> None:
        self.api_key = api_key or FRED_API_KEY
        self.fred = Fred(api_key=self.api_key)

    def get_cpi_data(self, start_year: int, end_year: int) -> pd.DataFrame:
        """Fetch CPI data for inflation adjustments."""
        series_id = "CPIAUCSL"  # Consumer Price Index for All Urban Consumers
        data = self.fred.get_series(
            series_id,
            observation_start=f"{start_year}-01-01",
            observation_end=f"{end_year}-12-31",
        )
        return data.resample("Y").mean()

    def get_economic_indicators(
        self,
        indicators: list[str],
        start_year: int,
        end_year: int,
    ) -> pd.DataFrame:
        """Fetch multiple economic indicators for analysis."""
        data = {}
        for indicator in indicators:
            series = self.fred.get_series(
                indicator,
                observation_start=f"{start_year}-01-01",
                observation_end=f"{end_year}-12-31",
            )
            data[indicator] = series.resample("Y").mean()

        return pd.DataFrame(data)
