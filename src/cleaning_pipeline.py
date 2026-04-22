"""Reusable cleaning pipeline for SmartCredit loan-default analytics.

This module is designed for auditability and repeatability so notebook logic
and script-based ETL stay aligned.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd


EXPECTED_COLUMNS: List[str] = [
    "LoanID",
    "Age",
    "Income",
    "LoanAmount",
    "CreditScore",
    "MonthsEmployed",
    "NumCreditLines",
    "InterestRate",
    "LoanTerm",
    "DTIRatio",
    "Education",
    "EmploymentType",
    "MaritalStatus",
    "HasMortgage",
    "HasDependents",
    "LoanPurpose",
    "HasCoSigner",
    "Default",
]

NUMERIC_COLUMNS: List[str] = [
    "Age",
    "Income",
    "LoanAmount",
    "CreditScore",
    "MonthsEmployed",
    "NumCreditLines",
    "InterestRate",
    "LoanTerm",
    "DTIRatio",
    "Default",
]

CATEGORICAL_COLUMNS: List[str] = [
    "Education",
    "EmploymentType",
    "MaritalStatus",
    "HasMortgage",
    "HasDependents",
    "LoanPurpose",
    "HasCoSigner",
]

YES_NO_COLUMNS: List[str] = ["HasMortgage", "HasDependents", "HasCoSigner"]


@dataclass(frozen=True)
class CleaningConfig:
    """Configuration for deterministic cleaning behavior."""

    enforce_numeric_bounds: bool = True
    cap_outliers_iqr: bool = True
    iqr_multiplier: float = 1.5
    create_missing_indicators: bool = True
    encode_binary_flags: bool = True


def _standardize_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip().str.title()

    yes_no_map = {
        "Yes": "Yes",
        "Y": "Yes",
        "True": "Yes",
        "1": "Yes",
        "No": "No",
        "N": "No",
        "False": "No",
        "0": "No",
    }
    for col in YES_NO_COLUMNS:
        if col in df.columns:
            df[col] = df[col].map(lambda v: yes_no_map.get(str(v), str(v)))

    return df


def _coerce_numeric(df: pd.DataFrame) -> pd.DataFrame:
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def _apply_bounds(df: pd.DataFrame) -> pd.DataFrame:
    bounds = {
        "Age": (18, 80),
        "Income": (0, None),
        "LoanAmount": (0, None),
        "CreditScore": (300, 900),
        "MonthsEmployed": (0, 600),
        "NumCreditLines": (0, 50),
        "InterestRate": (0, 100),
        "LoanTerm": (1, 480),
        "DTIRatio": (0, 1),
        "Default": (0, 1),
    }

    for col, (low, high) in bounds.items():
        if col not in df.columns:
            continue
        if low is not None:
            df.loc[df[col] < low, col] = np.nan
        if high is not None:
            df.loc[df[col] > high, col] = np.nan

    return df


def _cap_outliers_iqr(df: pd.DataFrame, cols: List[str], iqr_multiplier: float) -> pd.DataFrame:
    for col in cols:
        if col not in df.columns:
            continue
        series = df[col].dropna()
        if series.empty:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        low = q1 - iqr_multiplier * iqr
        high = q3 + iqr_multiplier * iqr
        df[col] = df[col].clip(lower=low, upper=high)
    return df


def _impute_missing(df: pd.DataFrame, create_missing_indicators: bool) -> pd.DataFrame:
    for col in NUMERIC_COLUMNS:
        if col in df.columns:
            if create_missing_indicators:
                df[f"{col}_was_missing"] = df[col].isna().astype(int)
            median_val = df[col].median()
            df[col] = df[col].fillna(median_val)

    for col in CATEGORICAL_COLUMNS:
        if col in df.columns:
            if create_missing_indicators:
                df[f"{col}_was_missing"] = df[col].isna().astype(int)
            mode_series = df[col].mode(dropna=True)
            fill_value = mode_series.iloc[0] if not mode_series.empty else "Unknown"
            df[col] = df[col].fillna(fill_value)

    return df


def _feature_engineering(df: pd.DataFrame, encode_binary_flags: bool) -> pd.DataFrame:
    if {"Income", "LoanAmount"}.issubset(df.columns):
        df["IncomeToLoanRatio"] = (df["Income"] / df["LoanAmount"]).replace([np.inf, -np.inf], np.nan)
        df["LoanToIncomeRatio"] = (df["LoanAmount"] / df["Income"]).replace([np.inf, -np.inf], np.nan)
        df["IncomeToLoanRatio"] = df["IncomeToLoanRatio"].fillna(0)
        df["LoanToIncomeRatio"] = df["LoanToIncomeRatio"].fillna(0)

    if {"InterestRate", "DTIRatio"}.issubset(df.columns):
        df["RateXDTI"] = df["InterestRate"] * df["DTIRatio"]

    if "CreditScore" in df.columns:
        df["CreditScoreBand"] = pd.cut(
            df["CreditScore"],
            bins=[299, 579, 669, 739, 799, 900],
            labels=["Poor", "Fair", "Good", "Very Good", "Excellent"],
            include_lowest=True,
        )

    if "DTIRatio" in df.columns:
        df["DTIBand"] = pd.cut(
            df["DTIRatio"],
            bins=[0, 0.2, 0.35, 0.5, 1.0],
            labels=["Low", "Moderate", "High", "Critical"],
            include_lowest=True,
        )

    if "LoanToIncomeRatio" in df.columns:
        df["LTI_Band"] = pd.cut(
            df["LoanToIncomeRatio"],
            bins=[0, 1, 2, 3, np.inf],
            labels=["Comfortable", "Watchlist", "Stretched", "Overleveraged"],
            include_lowest=True,
        )

    if {"CreditScoreBand", "DTIBand", "LTI_Band"}.issubset(df.columns):
        score_map = {
            "Poor": 4,
            "Fair": 3,
            "Good": 2,
            "Very Good": 1,
            "Excellent": 0,
            "Low": 0,
            "Moderate": 1,
            "High": 2,
            "Critical": 3,
            "Comfortable": 0,
            "Watchlist": 1,
            "Stretched": 2,
            "Overleveraged": 3,
        }
        risk_points = (
            df["CreditScoreBand"].astype("string").map(score_map).fillna(0)
            + df["DTIBand"].astype("string").map(score_map).fillna(0)
            + df["LTI_Band"].astype("string").map(score_map).fillna(0)
        )
        df["RiskPoints"] = risk_points
        df["RiskSegment"] = pd.cut(
            risk_points,
            bins=[-1, 2, 4, 6, np.inf],
            labels=["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"],
        )

    if encode_binary_flags:
        for col in YES_NO_COLUMNS:
            if col in df.columns:
                df[f"{col}_Flag"] = df[col].map({"Yes": 1, "No": 0}).fillna(0).astype(int)

    return df


def _create_cleaning_summary(before_df: pd.DataFrame, after_df: pd.DataFrame) -> pd.DataFrame:
    metrics = [
        {"metric": "rows_before", "value": int(len(before_df))},
        {"metric": "rows_after", "value": int(len(after_df))},
        {"metric": "duplicate_rows_before", "value": int(before_df.duplicated().sum())},
        {"metric": "duplicate_rows_after", "value": int(after_df.duplicated().sum())},
        {
            "metric": "duplicate_loanid_before",
            "value": int(before_df["LoanID"].duplicated().sum()) if "LoanID" in before_df.columns else -1,
        },
        {
            "metric": "duplicate_loanid_after",
            "value": int(after_df["LoanID"].duplicated().sum()) if "LoanID" in after_df.columns else -1,
        },
        {
            "metric": "missing_cells_before",
            "value": int(before_df.isna().sum().sum()),
        },
        {
            "metric": "missing_cells_after",
            "value": int(after_df.isna().sum().sum()),
        },
    ]

    if "Default" in after_df.columns:
        metrics.append(
            {
                "metric": "default_rate_after_pct",
                "value": round(float(after_df["Default"].mean() * 100), 4),
            }
        )

    return pd.DataFrame(metrics)


def clean_loan_data(df: pd.DataFrame, config: CleaningConfig | None = None) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """Clean SmartCredit loan data and return (cleaned_df, summary_df)."""
    cfg = config or CleaningConfig()
    before = df.copy()

    # Keep only known columns when present, but preserve extra columns too.
    ordered_cols = [c for c in EXPECTED_COLUMNS if c in df.columns] + [
        c for c in df.columns if c not in EXPECTED_COLUMNS
    ]
    df = df[ordered_cols].copy()

    # Row-level deduplication first, then normalize data types and categories.
    df = df.drop_duplicates().copy()
    df = _standardize_categoricals(df)
    df = _coerce_numeric(df)

    if cfg.enforce_numeric_bounds:
        df = _apply_bounds(df)

    if cfg.cap_outliers_iqr:
        outlier_cols = [
            "Income",
            "LoanAmount",
            "InterestRate",
            "DTIRatio",
            "LoanToIncomeRatio",
        ]
        df = _cap_outliers_iqr(df, outlier_cols, cfg.iqr_multiplier)

    df = _impute_missing(df, cfg.create_missing_indicators)
    df = _feature_engineering(df, cfg.encode_binary_flags)

    # Re-cap outliers for engineered ratio column after feature generation.
    if cfg.cap_outliers_iqr and "LoanToIncomeRatio" in df.columns:
        df = _cap_outliers_iqr(df, ["LoanToIncomeRatio"], cfg.iqr_multiplier)

    summary = _create_cleaning_summary(before, df)
    return df, summary
