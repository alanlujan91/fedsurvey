"""Central configuration for the fedsurvey package."""

from __future__ import annotations

from pathlib import Path
from typing import Final

# URLs and Data Sources
SCF_DATA_URL: Final = "https://www.federalreserve.gov/econres/files/"

# Year configurations
FIRST_YEAR: Final = 1989
LAST_YEAR: Final = 2022
INTERVAL: Final = 3

# File type mappings
FILE_TYPES: Final[dict[str, str]] = {
    "sas": ".zip",
    "stata": "s.zip",
    "csv": "excel.zip",
}

# Directory configurations
PKG_DIR: Final = Path(__file__).resolve().parent
DATA_DIR: Final = PKG_DIR / "data"
CACHE_DIR: Final = DATA_DIR / ".cache"

# Logging configuration
LOG_FORMAT: Final = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_LEVEL: Final = "INFO"

# Performance configurations
CHUNK_SIZE: Final = 10000
MAX_WORKERS: Final = 4
