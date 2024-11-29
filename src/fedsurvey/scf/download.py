from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import requests
from requests.exceptions import RequestException

from ..exceptions import DownloadError
from ..models import SCFMetadata

# Constants
SCF_DATA_URL = "https://www.federalreserve.gov/econres/files/"
DATA_DIR = Path(__file__).parent / "data"
FILE_TYPES = {
    "stata": "s.zip",
    "sas": "x.zip",
    "csv": "csv.zip",
}

VALID_YEARS = range(1989, 2023, 3)  # SCF is triennial


def setup_session() -> requests.Session:
    """Set up requests session with appropriate headers."""
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "fedsurvey/0.1.0",
            "Accept": "application/zip",
        },
    )
    return session


def download_year(year: int, file_type: str = "stata") -> Path:
    """Download SCF data for a specific year.

    Args:
    ----
        year: Survey year to download
        file_type: Type of file to download ('stata', 'sas', or 'csv')

    Returns:
    -------
        Path to the downloaded file

    Raises:
    ------
        DownloadError: If download fails
        ValueError: If year or file_type is invalid

    """
    try:
        if year not in VALID_YEARS:
            raise ValueError(
                f"Invalid year: {year}. Must be one of {list(VALID_YEARS)}",
            )

        if file_type not in FILE_TYPES:
            raise ValueError(
                f"Invalid file type: {file_type}. Must be one of {list(FILE_TYPES.keys())}",
            )

        return save_year_zip(year, file_type)

    except Exception as e:
        raise DownloadError(f"Failed to download data for {year}: {e}") from e


def save_year_zip(
    year: int,
    file_type: str = "stata",
    save_dir: Optional[Path] = None,
    session: Optional[requests.Session] = None,
) -> Path:
    """Download and save SCF data for a specific year.

    Args:
    ----
        year: Survey year to download
        file_type: Type of file to download ('stata', 'sas', or 'csv')
        save_dir: Directory to save the file (defaults to package data directory)
        session: Requests session to use for download

    Returns:
    -------
        Path to the downloaded file

    Raises:
    ------
        DownloadError: If download or save operations fail
        ValueError: If year or file_type is invalid

    """
    try:
        # Validate year before attempting download
        if year not in VALID_YEARS:
            raise ValueError(
                f"Invalid year: {year}. Must be one of {list(VALID_YEARS)}",
            )

        if save_dir is None:
            save_dir = DATA_DIR
        save_dir.mkdir(parents=True, exist_ok=True)

        file_name = f"scfp{year}{FILE_TYPES[file_type]}"
        save_path = save_dir / file_name

        if save_path.exists():
            logging.info(f"File already exists: {save_path}")
            return save_path

        session = session or setup_session()
        url = f"{SCF_DATA_URL}{file_name}"

        logging.info(f"Downloading {url} to {save_path}")
        response = session.get(url, stream=True)
        response.raise_for_status()

        with save_path.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # Create metadata
        metadata = SCFMetadata(
            year=year,
            file_type=file_type,
            record_count=0,  # This would be updated after processing
        )

        return save_path

    except RequestException as e:
        raise DownloadError(f"Failed to download {file_name}: {e}") from e


def download_all_years(
    file_type: str = "stata",
    years: Optional[list[int]] = None,
) -> list[Path]:
    """Download SCF data for multiple years.

    Args:
    ----
        file_type: Type of file to download ('stata', 'sas', or 'csv')
        years: List of years to download (defaults to all available years)

    Returns:
    -------
        List of paths to downloaded files

    Raises:
    ------
        DownloadError: If any download fails

    """
    if years is None:
        years = list(VALID_YEARS)

    paths = []
    session = setup_session()

    for year in years:
        try:
            path = save_year_zip(year, file_type, session=session)
            paths.append(path)
        except Exception as e:
            raise DownloadError(f"Failed to download data for {year}: {e}") from e

    return paths
