"""Analysis of household portfolio composition."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ..exceptions import ProcessingError


def analyze_portfolio_composition(
    df: pd.DataFrame,
    weight_col: str = "wgt",
    by_year: bool = True,
    by_percentile: bool = False,
    n_percentiles: int = 5,
) -> pd.DataFrame:
    """Analyze detailed portfolio composition following bulletin methodology.

    Components from bulletin:
    1. Transaction accounts (checking, savings, MMDA, call)
    2. Certificates of deposit
    3. Savings bonds
    4. Bonds (govt, corporate, municipal)
    5. Stocks (direct holdings)
    6. Mutual funds (stock, bond, mixed)
    7. Retirement accounts (IRA/Keogh, 401k/403b)
    8. Life insurance (cash value)
    9. Other managed assets (trusts, annuities)
    10. Other financial assets
    """
    try:
        # Define components from bulletin.macro
        components = {
            "transaction": ["checking", "savings", "mmda", "call"],
            "cds": ["cds"],
            "savings_bonds": ["savbnd"],
            "bonds": ["notxbnd", "mortbnd", "govtbnd", "obnd"],
            "stocks": ["stocks"],
            "mutual_funds": ["stmutf", "tfbmutf", "gbmutf", "obmutf", "comutf"],
            "retirement": ["retqliq"],
            "life_insurance": ["cashli"],
            "managed": ["othma"],
            "other_fin": ["othfin"],
        }

        def calc_shares(data: pd.DataFrame) -> pd.Series:
            """Calculate portfolio shares for a group."""
            total_assets = (data["fin"] * data[weight_col]).sum()
            shares = {}

            for comp_name, comp_vars in components.items():
                # Sum component values and weight by survey weights
                comp_sum = data[comp_vars].sum(axis=1)
                shares[f"{comp_name}_share"] = (
                    comp_sum * data[weight_col]
                ).sum() / total_assets

            return pd.Series(shares)

        # Calculate shares by group
        if by_year:
            result = df.groupby("year", observed=True).apply(
                calc_shares,
                include_groups=False,
            )
        else:
            result = calc_shares(df)

        # Optional percentile breakdown
        if by_percentile:
            if "fin" not in df.columns:
                raise KeyError("Financial assets column 'fin' not found")

            df = df.copy()  # Avoid SettingWithCopyWarning
            df["wealth_percentile"] = pd.qcut(
                df["fin"],
                q=n_percentiles,
                labels=[f"P{i+1}" for i in range(n_percentiles)],
            )
            result = df.groupby("wealth_percentile", observed=True).apply(
                calc_shares,
                include_groups=False,
            )

        return result

    except Exception as e:
        raise ProcessingError(f"Error analyzing portfolio composition: {e}")


def analyze_debt_composition(
    df: pd.DataFrame,
    weight_col: str = "wgt",
    by_year: bool = True,
) -> pd.DataFrame:
    """Analyze detailed debt composition following bulletin methodology.

    Components from bulletin:
    1. Home mortgages (first lien)
    2. Other residential property debt
    3. Credit card balances
    4. Vehicle loans
    5. Education loans
    6. Other lines of credit
    7. Other installment loans
    """
    try:
        # Components from bulletin.macro
        components = {
            "mortgages": ["nh_mort"],
            "other_res": ["resdbt"],
            "credit_card": ["ccbal"],
            "vehicle": ["veh_inst"],
            "education": ["edn_inst"],
            "other_loc": ["othloc"],
            "other_inst": ["oth_inst"],
        }

        def calc_shares(data: pd.DataFrame) -> pd.Series:
            """Calculate debt shares and payment ratios for a group."""
            total_debt = (data["debt"] * data[weight_col]).sum()
            shares = {}

            for comp_name, comp_vars in components.items():
                # Calculate weighted share of total debt
                comp_sum = data[comp_vars].sum(axis=1)
                shares[f"{comp_name}_share"] = (
                    comp_sum * data[weight_col]
                ).sum() / total_debt

                # Calculate payment-to-income ratios for mortgages and credit cards
                if comp_name in ["mortgages", "credit_card"]:
                    payment_col = f"pay{comp_name}"
                    if payment_col in data.columns:
                        monthly_income = data["income"] / 12
                        payment_ratio = data[payment_col] / monthly_income
                        shares[f"{comp_name}_pir"] = np.median(payment_ratio)

            return pd.Series(shares)

        if by_year:
            result = df.groupby("year", observed=True).apply(
                calc_shares,
                include_groups=False,
            )
        else:
            result = calc_shares(df)

        return result

    except Exception as e:
        raise ProcessingError(f"Error analyzing debt composition: {e}")
