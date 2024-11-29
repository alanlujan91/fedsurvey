"""Tests for plotting utilities."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import pytest
from fedsurvey.utils.plotting import weighted_relplot, wmean_lineplot, wmedian_lineplot


@pytest.fixture()
def sample_plot_data():
    """Create sample data for plotting tests."""
    np.random.seed(42)
    n = 100
    return pd.DataFrame(
        {
            "x": np.repeat(range(5), n // 5),
            "y": np.random.lognormal(0, 1, n),
            "style": np.repeat(["A", "B"], n // 2),
            "weights": np.random.uniform(0.5, 1.5, n),
            "col": np.repeat(["Group1", "Group2"], n // 2),
        },
    )


def test_wmedian_lineplot(sample_plot_data) -> None:
    """Test weighted median line plot."""
    plt.figure()
    plot = wmedian_lineplot(
        sample_plot_data,
        "x",
        "y",
        "weights",
        "style",
        errorbar=True,
    )

    assert plot is not None
    assert len(plot.get_lines()) > 0  # Has lines
    plt.close()


def test_wmean_lineplot(sample_plot_data) -> None:
    """Test weighted mean line plot."""
    plt.figure()
    plot = wmean_lineplot(sample_plot_data, "x", "y", "weights", "style", errorbar=True)

    assert plot is not None
    assert len(plot.get_lines()) > 0
    plt.close()


def test_weighted_relplot(sample_plot_data) -> None:
    """Test weighted relational plot."""
    plot = weighted_relplot(sample_plot_data, "x", "y", "weights", "col", "style")

    assert plot is not None
    assert len(plot.axes.flat) == 2  # Two subplots
    plt.close()


def test_plot_error_handling() -> None:
    """Test error handling in plotting functions."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})

    with pytest.raises(KeyError):
        wmedian_lineplot(invalid_df, "x", "y", "weights", "style")

    with pytest.raises(KeyError):
        wmean_lineplot(invalid_df, "x", "y", "weights", "style")

    with pytest.raises(KeyError):
        weighted_relplot(invalid_df, "x", "y", "weights", "col", "style")
