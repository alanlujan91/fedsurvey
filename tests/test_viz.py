"""Tests for visualization functions."""

from __future__ import annotations

import matplotlib as mpl
import numpy as np
import pandas as pd
import pytest

# Use Agg backend to avoid Tcl/Tk issues
mpl.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.figure import Figure

from fedsurvey.visualize import (
    plot_lorenz_curve,
    plot_wealth_distribution,
)
from fedsurvey.visualize.distribution import (
    plot_racial_wealth_gap,
    plot_wealth_composition_by_percentile,
    plot_wealth_composition_trends,
    plot_wealth_mobility_heatmap,
)


@pytest.fixture
def sample_viz_data() -> pd.DataFrame:
    """Create sample data for visualization testing."""
    np.random.seed(42)
    n_samples = 1000

    return pd.DataFrame(
        {
            "networth": np.random.lognormal(10, 2, n_samples),
            "networth_weighted": np.random.lognormal(10, 2, n_samples),
            "financial_assets": np.random.lognormal(8, 2, n_samples),
            "home_value": np.random.lognormal(9, 1.5, n_samples),
            "business_value": np.random.lognormal(7, 3, n_samples),
            "year": np.repeat([2019, 2022], n_samples // 2),
            "race_label": np.random.choice(
                ["White non-Hispanic", "Black", "Hispanic"],
                n_samples,
                p=[0.6, 0.2, 0.2],
            ),
            "wgt": np.random.uniform(0.5, 1.5, n_samples),
        },
    )


def test_plot_wealth_distribution(sample_viz_data: pd.DataFrame) -> None:
    """Test wealth distribution plotting."""
    fig = plot_wealth_distribution(sample_viz_data)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1

    # Test log scale
    fig = plot_wealth_distribution(sample_viz_data, log_scale=True)
    assert fig.axes[0].get_xscale() == "log"

    plt.close("all")


def test_plot_lorenz_curve(sample_viz_data: pd.DataFrame) -> None:
    """Test Lorenz curve plotting."""
    fig = plot_lorenz_curve(sample_viz_data)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1

    # Check line of perfect equality
    lines = fig.axes[0].get_lines()
    assert len(lines) >= 2  # At least Lorenz curve and equality line

    plt.close("all")


def test_plot_wealth_composition_trends(sample_viz_data: pd.DataFrame) -> None:
    """Test wealth composition trend plotting."""
    components = ["financial_assets", "home_value", "business_value"]
    fig = plot_wealth_composition_trends(sample_viz_data, components)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1

    # Test stacked area plot
    assert fig.axes[0].get_children()[0].__class__.__name__ == "PolyCollection"

    plt.close("all")


def test_plot_racial_wealth_gap(sample_viz_data: pd.DataFrame) -> None:
    """Test racial wealth gap plotting."""
    fig = plot_racial_wealth_gap(sample_viz_data)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1

    # Check reference line at 1.0
    lines = fig.axes[0].get_lines()
    assert any(np.allclose(line.get_ydata(), 1.0) for line in lines)

    plt.close("all")


def test_plot_wealth_mobility_heatmap(sample_viz_data: pd.DataFrame) -> None:
    """Test wealth mobility heatmap plotting."""
    fig = plot_wealth_mobility_heatmap(sample_viz_data)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 2  # Main heatmap and colorbar

    plt.close("all")


def test_plot_wealth_composition_by_percentile(sample_viz_data: pd.DataFrame) -> None:
    """Test wealth composition percentile plotting."""
    components = ["financial_assets", "home_value", "business_value"]
    fig = plot_wealth_composition_by_percentile(sample_viz_data, components)

    assert isinstance(fig, Figure)
    assert len(fig.axes) == 1

    plt.close("all")


def test_visualization_customization() -> None:
    """Test visualization customization options."""
    data = pd.DataFrame(
        {"networth": np.random.lognormal(10, 2, 100), "wgt": np.ones(100)},
    )

    # Test figure size customization
    fig = plot_wealth_distribution(data, figsize=(12, 8))
    assert fig.get_size_inches().tolist() == [12, 8]

    # Test style customization using a valid style
    plt.style.use("seaborn-v0_8")
    fig = plot_wealth_distribution(data)
    assert plt.style.available[-1] == "seaborn-v0_8"

    plt.close("all")


def test_empty_data_handling() -> None:
    """Test visualization handling of empty data."""
    empty_df = pd.DataFrame(columns=["networth", "wgt"])

    with pytest.raises((ValueError, RuntimeError)):
        plot_wealth_distribution(empty_df)

    plt.close("all")
