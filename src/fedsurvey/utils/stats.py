"""Statistical utility functions."""

from __future__ import annotations

import warnings

import numpy as np


def weighted_quantile(values: np.ndarray, weights: np.ndarray, q: float) -> float:
    """Calculate weighted quantile.

    Args:
    ----
        values: Array of values
        weights: Array of weights
        q: Quantile to compute (0 to 1)

    Returns:
    -------
        Weighted quantile value

    """
    if weights is None:
        weights = np.ones_like(values)

    if len(values) != len(weights):
        msg = "Values and weights must be same length"
        raise ValueError(msg)

    if len(values) == 0:
        return np.nan

    if len(values) == 1:
        return values[0]

    # Sort values and weights together
    values = np.asarray(values)
    weights = np.asarray(weights)
    sorted_idx = np.argsort(values)
    sorted_values = values[sorted_idx]
    sorted_weights = weights[sorted_idx]

    # Calculate cumulative weights
    cumsum = np.cumsum(sorted_weights)

    # Handle zero weights
    if cumsum[-1] == 0:
        warnings.warn(
            "All weights are zero",
            RuntimeWarning,
            stacklevel=2,
        )
        return np.nan

    # Normalize cumulative weights
    cumsum = cumsum / cumsum[-1]

    # Find index where cumsum exceeds q
    idx = np.searchsorted(cumsum, q, side="right")

    # Handle edge cases
    if idx == 0:
        return sorted_values[0]
    if idx == len(values):
        return sorted_values[-1]

    # Get interpolation points
    i0, i1 = idx - 1, idx
    v0, v1 = sorted_values[i0], sorted_values[i1]
    c0, c1 = cumsum[i0], cumsum[i1]

    # Linear interpolation
    return v0 + (v1 - v0) * (q - c0) / (c1 - c0)


def weighted_mean(values: np.ndarray, weights: np.ndarray | None = None) -> float:
    """Calculate weighted mean.

    Args:
    ----
        values: Array of values
        weights: Optional array of weights

    Returns:
    -------
        Weighted mean value

    """
    if weights is None:
        return np.mean(values)

    if len(values) != len(weights):
        msg = "Values and weights must be same length"
        raise ValueError(msg)

    if len(values) == 0:
        return np.nan

    if len(values) == 1:
        return values[0]

    # Handle zero weights
    if np.sum(weights) == 0:
        warnings.warn(
            "All weights are zero",
            RuntimeWarning,
            stacklevel=2,
        )
        return np.nan

    values = np.asarray(values)
    weights = np.asarray(weights)
    return np.sum(values * weights) / np.sum(weights)


def weighted_std(values: np.ndarray, weights: np.ndarray | None = None) -> float:
    """Calculate weighted standard deviation.

    Args:
    ----
        values: Array of values
        weights: Optional array of weights

    Returns:
    -------
        Weighted standard deviation

    """
    if weights is None:
        return np.std(values)

    if len(values) != len(weights):
        msg = "Values and weights must be same length"
        raise ValueError(msg)

    if len(values) == 0 or len(values) == 1:
        return 0.0

    # Handle zero weights
    if np.sum(weights) == 0:
        warnings.warn(
            "All weights are zero",
            RuntimeWarning,
            stacklevel=2,
        )
        return np.nan

    values = np.asarray(values)
    weights = np.asarray(weights)
    mean = weighted_mean(values, weights)
    variance = weighted_mean((values - mean) ** 2, weights)
    return np.sqrt(variance)


def calculate_top_share(
    values: np.ndarray,
    weights: np.ndarray,
    share: float,
) -> float:
    """Calculate share of total held by top X%.

    Args:
    ----
        values: Array of values
        weights: Array of weights
        share: Share threshold (0 to 1)

    Returns:
    -------
        Share of total held by top share of population

    """
    if weights is None:
        weights = np.ones_like(values)

    if len(values) != len(weights):
        msg = "Values and weights must be same length"
        raise ValueError(msg)

    if len(values) == 0:
        return np.nan

    if len(values) == 1:
        return 1.0

    # Handle zero weights
    if np.sum(weights) == 0:
        warnings.warn(
            "All weights are zero",
            RuntimeWarning,
            stacklevel=2,
        )
        return np.nan

    values = np.asarray(values)
    weights = np.asarray(weights)

    # Sort by values in descending order
    sorted_idx = np.argsort(values)[::-1]
    sorted_values = values[sorted_idx]
    sorted_weights = weights[sorted_idx]

    # Calculate cumulative weights
    cumsum = np.cumsum(sorted_weights)
    cumsum = cumsum / cumsum[-1]

    # Find cutoff point
    cutoff_idx = np.searchsorted(cumsum, share)

    # Calculate share
    top_total = np.sum(sorted_values[:cutoff_idx] * sorted_weights[:cutoff_idx])
    total = np.sum(sorted_values * sorted_weights)

    return top_total / total


def gini_coefficient(values: np.ndarray, weights: np.ndarray | None = None) -> float:
    """Calculate the Gini coefficient of inequality."""
    if weights is None:
        weights = np.ones_like(values)

    # Handle empty arrays
    if len(values) == 0:
        return 0.0

    # Handle single value
    if len(values) == 1:
        return 0.0

    # Handle uniform distribution
    if np.allclose(values, values[0]):
        return 0.0

    # Sort values and weights together
    sorted_indices = np.argsort(values)
    values = values[sorted_indices]
    weights = weights[sorted_indices]

    # Calculate weighted cumulative shares
    cum_weights = np.cumsum(weights)
    cum_values = np.cumsum(values * weights)
    total_weight = cum_weights[-1]
    total_value = cum_values[-1]

    # Handle zero weights or values
    if total_weight == 0 or total_value == 0:
        return 0.0

    # Normalize cumulative shares
    cum_share_weights = cum_weights / total_weight
    cum_share_values = cum_values / total_value

    # Calculate Gini coefficient using trapezoidal rule
    # G = 1 - 2 * area under Lorenz curve
    return max(0.0, 1.0 - 2.0 * np.trapezoid(cum_share_values, cum_share_weights))
