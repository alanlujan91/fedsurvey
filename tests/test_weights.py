"""Tests for weight adjustment utilities."""

from __future__ import annotations

import pandas as pd
import pytest
from fedsurvey.exceptions import ProcessingError
from fedsurvey.utils.weights import adjust_influential_weights, apply_replicate_weights


def test_replicate_weights():
    """Test replicate weight adjustments."""
    df = pd.DataFrame({"wgt": [1.0, 2.0, 3.0]})

    result = apply_replicate_weights(df)
    assert all(result["wgt_adj"] == df["wgt"] / 5)


def test_replicate_weights_missing_column():
    """Test handling of missing weight column."""
    df = pd.DataFrame({"other": [1, 2, 3]})

    with pytest.raises(ProcessingError):
        apply_replicate_weights(df)


def test_influential_weights():
    """Test influential case weight adjustments."""
    df = pd.DataFrame(
        {
            "networth": [1e6, 1e3, 1e3],
            "fin": [5e5, 5e2, 5e2],
            "nfin": [5e5, 5e2, 5e2],
            "debt": [0, 0, 0],
            "wgt": [1.0, 1.0, 1.0],
        },
    )

    result = adjust_influential_weights(df, threshold=0.5)

    # First case should be dampened
    assert result.loc[0, "wgt"] < df.loc[0, "wgt"]
    # Other cases should be unchanged
    assert result.loc[1:, "wgt"].equals(df.loc[1:, "wgt"])
