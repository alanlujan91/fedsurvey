"""Custom exceptions for fedsurvey package."""

from __future__ import annotations


class FedSurveyError(Exception):
    """Base exception for fedsurvey package."""


class DownloadError(FedSurveyError):
    """Error downloading SCF data."""


class ProcessingError(FedSurveyError):
    """Error processing SCF data."""


class ValidationError(FedSurveyError):
    """Error validating SCF data."""


class MergeError(FedSurveyError):
    """Error merging SCF data."""
