"""Statistical analysis utilities for SmartCredit (Phase 7)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, List, Tuple

import numpy as np
import pandas as pd
from scipy.stats import chi2_contingency, ttest_ind
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import statsmodels.api as sm


NUMERIC_CANDIDATES: List[str] = [
    "Age",
    "Income",
    "LoanAmount",
    "CreditScore",
    "MonthsEmployed",
    "NumCreditLines",
    "InterestRate",
    "LoanTerm",
    "DTIRatio",
    "IncomeToLoanRatio",
    "LoanToIncomeRatio",
    "RateXDTI",
]

CATEGORICAL_CANDIDATES: List[str] = [
    "Education",
    "EmploymentType",
    "MaritalStatus",
    "HasMortgage",
    "HasDependents",
    "LoanPurpose",
    "HasCoSigner",
    "CreditScoreBand",
    "DTIBand",
    "LTI_Band",
    "RiskSegment",
]


@dataclass(frozen=True)
class StatisticalOutputs:
    correlation_df: pd.DataFrame
    ttest_df: pd.DataFrame
    chi_square_df: pd.DataFrame
    logit_coef_df: pd.DataFrame
    feature_importance_df: pd.DataFrame
    scored_df: pd.DataFrame
    model_perf_df: pd.DataFrame


def _default_col(df: pd.DataFrame) -> str:
    if "Default" not in df.columns:
        raise ValueError("Target column 'Default' is required.")
    return "Default"


def correlation_with_target(df: pd.DataFrame, target: str = "Default") -> pd.DataFrame:
    numeric_cols = [c for c in NUMERIC_CANDIDATES if c in df.columns] + [target]
    numeric_cols = list(dict.fromkeys(numeric_cols))
    corr = df[numeric_cols].corr(numeric_only=True)[target].drop(target).sort_values(ascending=False)
    return corr.rename("correlation").reset_index().rename(columns={"index": "feature"})


def hypothesis_ttests(df: pd.DataFrame, target: str = "Default") -> pd.DataFrame:
    rows = []
    for col in [c for c in NUMERIC_CANDIDATES if c in df.columns]:
        g1 = df.loc[df[target] == 1, col].dropna()
        g0 = df.loc[df[target] == 0, col].dropna()
        if len(g1) < 2 or len(g0) < 2:
            continue
        t_stat, p_val = ttest_ind(g1, g0, equal_var=False)
        rows.append(
            {
                "feature": col,
                "mean_default": round(float(g1.mean()), 6),
                "mean_non_default": round(float(g0.mean()), 6),
                "mean_diff": round(float(g1.mean() - g0.mean()), 6),
                "t_stat": round(float(t_stat), 6),
                "p_value": float(p_val),
                "significant_5pct": bool(p_val < 0.05),
            }
        )
    return pd.DataFrame(rows).sort_values("p_value", ascending=True)


def chi_square_tests(df: pd.DataFrame, target: str = "Default") -> pd.DataFrame:
    rows = []
    for col in [c for c in CATEGORICAL_CANDIDATES if c in df.columns]:
        table = pd.crosstab(df[col], df[target])
        if table.shape[0] < 2 or table.shape[1] < 2:
            continue
        chi2, p_val, dof, _ = chi2_contingency(table)
        n = table.values.sum()
        phi2 = chi2 / max(n, 1)
        r, k = table.shape
        cramers_v = np.sqrt(phi2 / max(min(k - 1, r - 1), 1))
        rows.append(
            {
                "feature": col,
                "chi2": round(float(chi2), 6),
                "p_value": float(p_val),
                "dof": int(dof),
                "cramers_v": round(float(cramers_v), 6),
                "significant_5pct": bool(p_val < 0.05),
            }
        )
    return pd.DataFrame(rows).sort_values("p_value", ascending=True)


def _model_matrix(df: pd.DataFrame, target: str = "Default") -> Tuple[pd.DataFrame, pd.Series, pd.Series]:
    id_series = df["LoanID"] if "LoanID" in df.columns else pd.Series(np.arange(len(df)), name="LoanID")

    feature_cols = [c for c in df.columns if c not in {target, "LoanID"}]
    x = df[feature_cols].copy()

    # Use robust object handling with one-hot encoding.
    obj_cols = x.select_dtypes(include=["object", "category", "string"]).columns
    for c in obj_cols:
        x[c] = x[c].astype("string").fillna("Unknown")

    x = pd.get_dummies(x, drop_first=True)
    x = x.replace([np.inf, -np.inf], np.nan).fillna(0)

    y = pd.to_numeric(df[target], errors="coerce").fillna(0).astype(int)
    return x, y, id_series


def logistic_model_and_scores(df: pd.DataFrame, target: str = "Default") -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    x, y, loan_ids = _model_matrix(df, target=target)

    x_train, x_test, y_train, y_test, id_train, id_test = train_test_split(
        x,
        y,
        loan_ids,
        test_size=0.25,
        random_state=42,
        stratify=y,
    )

    scaler = StandardScaler(with_mean=False)
    x_train_scaled = scaler.fit_transform(x_train)
    x_test_scaled = scaler.transform(x_test)

    clf = LogisticRegression(max_iter=600, class_weight="balanced")
    clf.fit(x_train_scaled, y_train)

    pred_test = clf.predict_proba(x_test_scaled)[:, 1]
    pred_all = clf.predict_proba(scaler.transform(x))[:, 1]

    auc = roc_auc_score(y_test, pred_test)
    pr_auc = average_precision_score(y_test, pred_test)

    perf_df = pd.DataFrame(
        [
            {"metric": "roc_auc", "value": round(float(auc), 6)},
            {"metric": "pr_auc", "value": round(float(pr_auc), 6)},
            {"metric": "test_rows", "value": int(len(x_test))},
            {"metric": "train_rows", "value": int(len(x_train))},
        ]
    )

    importance_df = pd.DataFrame(
        {
            "feature": x.columns,
            "coefficient": clf.coef_.flatten(),
        }
    )
    importance_df["abs_coefficient"] = importance_df["coefficient"].abs()
    importance_df = importance_df.sort_values("abs_coefficient", ascending=False)

    scored_df = pd.DataFrame(
        {
            "LoanID": loan_ids.values,
            "actual_default": y.values,
            "default_probability": pred_all,
        }
    )
    scored_df["risk_band"] = pd.qcut(
        scored_df["default_probability"],
        q=5,
        labels=["Very Low", "Low", "Medium", "High", "Very High"],
    )

    return perf_df, importance_df, scored_df


def logit_significance(df: pd.DataFrame, target: str = "Default") -> pd.DataFrame:
    x, y, _ = _model_matrix(df, target=target)
    x = sm.add_constant(x, has_constant="add")
    model = sm.Logit(y, x).fit(disp=False)

    coef_df = pd.DataFrame(
        {
            "feature": model.params.index,
            "coefficient": model.params.values,
            "p_value": model.pvalues.values,
        }
    )
    coef_df["odds_ratio"] = np.exp(coef_df["coefficient"])
    coef_df["significant_5pct"] = coef_df["p_value"] < 0.05
    coef_df = coef_df.sort_values("p_value", ascending=True)
    return coef_df


def run_full_statistical_analysis(df: pd.DataFrame) -> StatisticalOutputs:
    target = _default_col(df)

    corr_df = correlation_with_target(df, target=target)
    ttest_df = hypothesis_ttests(df, target=target)
    chi_df = chi_square_tests(df, target=target)
    logit_df = logit_significance(df, target=target)
    perf_df, importance_df, scored_df = logistic_model_and_scores(df, target=target)

    return StatisticalOutputs(
        correlation_df=corr_df,
        ttest_df=ttest_df,
        chi_square_df=chi_df,
        logit_coef_df=logit_df,
        feature_importance_df=importance_df,
        scored_df=scored_df,
        model_perf_df=perf_df,
    )
