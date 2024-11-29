"""SCF data handling modules."""

from __future__ import annotations

from .categorize import categorize_income, categorize_work_status
from .clean import adjust_for_inflation, apply_weights, harmonize_variables
from .download import download_all_years, download_year
from .harmonize import harmonize_variables
from .merge import merge_files
from .race import harmonize_race

__all__ = [
    "categorize_income",
    "categorize_work_status",
    "harmonize_variables",
    "adjust_for_inflation",
    "apply_weights",
    "download_year",
    "download_all_years",
    "harmonize_variables",
    "merge_files",
    "harmonize_race",
]
