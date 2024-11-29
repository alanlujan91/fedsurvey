"""Tests for statistical analysis functions."""

from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from fedsurvey.analysis import calculate_percentiles, gini_coefficient, wealth_shares
from fedsurvey.analysis.demographics import (
    intersectional_wealth_gap,
    racial_wealth_gap,
    wealth_by_education,
)
from fedsurvey.analysis.trends import (
    concentration_trends,
    mobility_analysis,
    wealth_growth_rates,
    wealth_mobility,
)
from fedsurvey.analysis.wealth import (
    detailed_wealth_composition,
    wealth_composition,
)
from fedsurvey.exceptions import ProcessingError
from fedsurvey.viz.distribution import (
    plot_racial_wealth_gap,
    plot_wealth_composition_by_percentile,
    plot_wealth_composition_trends,
    plot_wealth_mobility_heatmap,
)
from matplotlib.figure import Figure


@pytest.fixture()
def sample_data() -> pd.DataFrame:
    """Create sample data for testing."""
    np.random.seed(42)
    n = 1000
    years = [2019, 2022]
    data = []

    for year in years:
        # Generate correlated data
        networth = np.random.lognormal(10, 2, n // 2)
        financial_assets = networth * np.random.beta(2, 5, n // 2)
        business_value = networth * np.random.beta(1, 10, n // 2)
        home_value = networth * np.random.beta(3, 4, n // 2)
        retirement_accounts = networth * np.random.beta(2, 6, n // 2)
        income = np.random.lognormal(8, 1, n // 2)

        # Demographics
        education_labels = np.random.choice(
            ["Less than HS", "HS grad", "College grad"],
            n // 2,
            p=[0.2, 0.5, 0.3],
        )
        race_labels = np.random.choice(
            ["White non-Hispanic", "Black", "Hispanic", "Other"],
            n // 2,
            p=[0.6, 0.15, 0.15, 0.1],
        )

        data.append(
            pd.DataFrame(
                {
                    "year": year,
                    "networth": networth,
                    "financial_assets": financial_assets,
                    "business_value": business_value,
                    "home_value": home_value,
                    "retirement_accounts": retirement_accounts,
                    "income": income,
                    "education_label": education_labels,
                    "race_label": race_labels,
                    "wgt": np.random.uniform(0.5, 1.5, n // 2),
                    "fin": financial_assets,
                    "nfin": home_value + business_value,
                    "debt": networth * 0.1,
                },
            ),
        )

    return pd.concat(data, ignore_index=True)


@pytest.fixture()
def empty_data() -> pd.DataFrame:
    """Create empty DataFrame with correct columns."""
    return pd.DataFrame(
        columns=[
            "year",
            "networth",
            "financial_assets",
            "income",
            "education_label",
            "race_label",
            "wgt",
        ],
    )


def test_calculate_percentiles(sample_data: pd.DataFrame) -> None:
    """Test percentile calculations."""
    result = calculate_percentiles(sample_data, "networth", "wgt", [10, 50, 90])

    assert isinstance(result, dict)
    assert all(0 <= p <= 100 for p in result.keys())
    assert result[10] < result[50] < result[90]


def test_gini_coefficient(sample_data: pd.DataFrame) -> None:
    """Test Gini coefficient calculation."""
    gini = gini_coefficient(sample_data["networth"].values, sample_data["wgt"].values)

    assert isinstance(gini, float)
    assert 0 <= gini <= 1

    # Test with uniform distribution
    uniform_data = np.ones(100)
    uniform_gini = gini_coefficient(uniform_data)
    assert np.isclose(uniform_gini, 0, atol=1e-10)


def test_wealth_shares(sample_data: pd.DataFrame) -> None:
    """Test wealth share calculations."""
    shares = wealth_shares(sample_data)

    assert isinstance(shares, dict)
    assert all(0 <= share <= 1 for share in shares.values())
    assert all(
        shares[k1] >= shares[k2]
        for k1, k2 in zip(shares.keys(), list(shares.keys())[1:])
    )


def test_wealth_by_education_normalized(sample_data: pd.DataFrame) -> None:
    """Test normalized education wealth analysis."""
    result = wealth_by_education(sample_data, normalize=True)

    assert isinstance(result, pd.DataFrame)
    assert all(
        measure in result.index
        for measure in ["networth", "financial_assets", "income"]
    )
    assert np.allclose(result.mean(axis=1), 1.0, rtol=1e-10)


def test_racial_wealth_gap_by_year(sample_data: pd.DataFrame) -> None:
    """Test racial wealth gap analysis with yearly breakdown."""
    result = racial_wealth_gap(sample_data, by_year=True)

    assert isinstance(result, pd.DataFrame)
    assert len(result.index.levels[0]) == len(sample_data["year"].unique())
    assert all(result.values.flatten() > 0)


def test_intersectional_wealth_gap_complete(sample_data: pd.DataFrame) -> None:
    """Test comprehensive intersectional analysis."""
    result = intersectional_wealth_gap(
        sample_data,
        primary_group="race_label",
        secondary_group="education_label",
    )

    assert isinstance(result, pd.DataFrame)
    expected_combinations = len(sample_data["race_label"].unique()) * len(
        sample_data["education_label"].unique(),
    )
    assert len(result) <= expected_combinations


def test_wealth_growth_rates_complete(sample_data: pd.DataFrame) -> None:
    """Test comprehensive growth rate analysis."""
    result = wealth_growth_rates(
        sample_data,
        measures=["networth", "income", "financial_assets"],
        percentiles=[10, 25, 50, 75, 90],
    )

    assert isinstance(result, pd.DataFrame)
    assert all(
        col.startswith(("networth", "income", "financial_assets"))
        for col in result.columns
    )
    # One growth rate period (2022 relative to 2019)
    assert len(result.dropna()) == 1


def test_concentration_trends_detailed(sample_data: pd.DataFrame) -> None:
    """Test detailed concentration trend analysis."""
    result = concentration_trends(
        sample_data,
        measures=["networth", "financial_assets", "home_value"],
        top_shares=[0.01, 0.05, 0.1, 0.5],
    )

    assert isinstance(result, pd.DataFrame)
    assert all(0 <= val <= 1 for val in result.values.flatten())
    assert len(result.columns) == 12  # 3 measures * 4 top shares


def test_mobility_analysis_edge_cases(sample_data: pd.DataFrame) -> None:
    """Test mobility analysis with edge cases."""
    years = sorted(sample_data["year"].unique())

    # Test with different numbers of quantiles
    for n_quantiles in [3, 5, 10]:
        result = mobility_analysis(sample_data, years[0], years[1], n_quantiles)
        assert result.shape == (n_quantiles, n_quantiles)
        # Each row should sum to 1 (if not empty)
        assert all(
            np.allclose(row.sum(), 1) if row.sum() > 0 else True
            for _, row in result.iterrows()
        )


def test_wealth_mobility_by_group(sample_data: pd.DataFrame) -> None:
    """Test wealth mobility with demographic breakdown."""
    result = wealth_mobility(sample_data, by_group="education_label")

    assert isinstance(result, pd.DataFrame)
    assert all(0 <= val <= 1 for val in result.values.flatten() if not pd.isna(val))


def test_wealth_composition_by_group(sample_data: pd.DataFrame) -> None:
    """Test wealth composition with group breakdown."""
    result = wealth_composition(
        sample_data,
        components=["financial_assets", "business_value", "home_value"],
        by_group="education_label",
    )

    assert isinstance(result, pd.DataFrame)
    assert all(0 <= val <= 1 for val in result.values.flatten())


def test_plot_wealth_composition_trends_customization(
    sample_data: pd.DataFrame,
) -> None:
    """Test wealth composition trend plotting with customization."""
    fig = plot_wealth_composition_trends(
        sample_data,
        components=["financial_assets", "home_value", "business_value"],
        figsize=(15, 8),
    )

    assert isinstance(fig, Figure)
    assert fig.get_size_inches().tolist() == [15, 8]


def test_plot_racial_wealth_gap_multiple_measures(sample_data: pd.DataFrame) -> None:
    """Test racial wealth gap plotting with multiple measures."""
    fig = plot_racial_wealth_gap(
        sample_data,
        measures=["networth", "income", "financial_assets"],
    )

    assert isinstance(fig, Figure)


def test_plot_wealth_mobility_heatmap_customization(sample_data: pd.DataFrame) -> None:
    """Test wealth mobility heatmap with customization."""
    fig = plot_wealth_mobility_heatmap(
        sample_data,
        measure="financial_assets",
        n_quantiles=4,
        cmap="viridis",
    )

    assert isinstance(fig, Figure)


def test_empty_dataframe(empty_data: pd.DataFrame) -> None:
    """Test handling of empty DataFrames."""
    with pytest.raises(ProcessingError):
        wealth_by_education(empty_data)

    with pytest.raises(ProcessingError):
        racial_wealth_gap(empty_data)

    with pytest.raises(ProcessingError):
        wealth_composition(empty_data)


def test_invalid_inputs() -> None:
    """Test handling of invalid inputs."""
    invalid_df = pd.DataFrame({"col1": [1, 2, 3]})  # Missing required columns

    with pytest.raises(ProcessingError):
        wealth_by_education(invalid_df)

    with pytest.raises(ProcessingError):
        racial_wealth_gap(invalid_df)

    with pytest.raises(ProcessingError):
        wealth_composition(invalid_df)


def test_negative_values(sample_data: pd.DataFrame) -> None:
    """Test handling of negative values."""
    sample_data.loc[0, "networth"] = -1000

    # Should handle negative values gracefully
    result = wealth_composition(sample_data)
    assert isinstance(result, pd.DataFrame)
