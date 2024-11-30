"""Tests for the download module."""

from __future__ import annotations

import pytest
import responses

from fedsurvey.core.config import SCF_DATA_URL
from fedsurvey.scf.download import DownloadError, save_year_zip


@pytest.fixture
def mock_session():
    with responses.RequestsMock() as rsps:
        yield rsps


def test_save_year_zip_success(mock_session, tmp_path) -> None:
    year = 2019
    file_name = "scfp2019s.zip"
    mock_session.add(
        responses.GET,
        f"{SCF_DATA_URL}{file_name}",
        body=b"mock data",
        status=200,
    )

    result = save_year_zip(year, save_dir=tmp_path)
    assert result.exists()
    assert result.name == file_name


def test_save_year_zip_invalid_year() -> None:
    with pytest.raises(ValueError, match="Invalid year"):
        save_year_zip(1900)


def test_save_year_zip_download_error(mock_session) -> None:
    mock_session.add(
        responses.GET,
        f"{SCF_DATA_URL}scfp2019s.zip",
        status=404,
    )

    with pytest.raises(DownloadError):
        save_year_zip(2019)
