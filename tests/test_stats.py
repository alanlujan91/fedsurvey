"""Tests for statistical utility functions."""

from __future__ import annotations

import numpy as np
import pytest

from fedsurvey.utils.stats import weighted_mean, weighted_quantile, weighted_std


def test_weighted_quantile() -> None:
    """Test weighted quantile calculation."""
    values = np.array([1, 2, 3, 4, 5])
    weights = np.array([1, 1, 2, 1, 1])

    # Median should be 2.5 with these weights
    # (2 + 3) / 2 since cumulative weight at 2 is 0.333 and at 3 is 0.667
    result = weighted_quantile(values, weights, 0.5)
    assert result == 2.5

    # 75th percentile
    result = weighted_quantile(values, weights, 0.75)
    assert 3 < result <= 4


def test_weighted_mean() -> None:
    """Test weighted mean calculation."""
    values = np.array([1, 2, 3, 4, 5])
    weights = np.array([1, 1, 2, 1, 1])

    result = weighted_mean(values, weights)
    expected = (1 * 1 + 2 * 1 + 3 * 2 + 4 * 1 + 5 * 1) / 6
    assert np.isclose(result, expected)


def test_weighted_std() -> None:
    """Test weighted standard deviation calculation."""
    values = np.array([1, 2, 3, 4, 5])
    weights = np.array([1, 1, 2, 1, 1])

    result = weighted_std(values, weights)
    assert result > 0

    # Test with uniform weights
    uniform_result = weighted_std(values)
    assert uniform_result > 0


def test_edge_cases() -> None:
    """Test edge cases for statistical functions."""
    # Single value
    assert weighted_quantile(np.array([1]), np.array([1]), 0.5) == 1
    assert weighted_mean(np.array([1])) == 1
    assert weighted_std(np.array([1])) == 0

    # Zero weights
    with pytest.warns(RuntimeWarning):
        weighted_mean(np.array([1, 2]), np.array([0, 0]))
