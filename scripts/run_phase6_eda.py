"""Run Phase 6 EDA and visual analysis for SmartCredit.

Generates:
- 20 high-value static charts (PNG)
- Interactive Plotly charts (HTML)
- EDA summary tables for reporting and Tableau storyboarding

Usage:
    python scripts/run_phase6_eda.py
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Dict

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly.express as px
import seaborn as sns


def _prepare_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    # Ensure expected derived columns exist for consistent Phase 6 outputs.
    if "CreditScoreBand" not in df.columns and "CreditScore" in df.columns:
        df["CreditScoreBand"] = pd.cut(
            df["CreditScore"],
            bins=[299, 579, 669, 739, 799, 900],
            labels=["Poor", "Fair", "Good", "Very Good", "Excellent"],
            include_lowest=True,
        )

    if "DTIBand" not in df.columns and "DTIRatio" in df.columns:
        df["DTIBand"] = pd.cut(
            df["DTIRatio"],
            bins=[0, 0.2, 0.35, 0.5, 1.0],
            labels=["Low", "Moderate", "High", "Critical"],
            include_lowest=True,
        )

    if "IncomeToLoanRatio" not in df.columns and {"Income", "LoanAmount"}.issubset(df.columns):
        df["IncomeToLoanRatio"] = (df["Income"] / df["LoanAmount"]).replace([np.inf, -np.inf], np.nan).fillna(0)

    if "RiskSegment" not in df.columns and {"CreditScoreBand", "DTIBand"}.issubset(df.columns):
        score_map = {
            "Poor": 3,
            "Fair": 2,
            "Good": 1,
            "Very Good": 0,
            "Excellent": 0,
            "Low": 0,
            "Moderate": 1,
            "High": 2,
            "Critical": 3,
        }
        points = (
            df["CreditScoreBand"].astype("string").map(score_map).fillna(0)
            + df["DTIBand"].astype("string").map(score_map).fillna(0)
        )
        df["RiskSegment"] = pd.cut(
            points,
            bins=[-1, 1, 3, 5, np.inf],
            labels=["Low Risk", "Moderate Risk", "High Risk", "Very High Risk"],
        )

    return df


def _safe_savefig(path: Path) -> None:
    plt.tight_layout()
    plt.savefig(path, dpi=170)
    plt.close()


def _default_rate_by(df: pd.DataFrame, col: str) -> pd.DataFrame:
    out = (
        df.groupby(col, dropna=False, as_index=False)
        .agg(loans=("Default", "size"), defaults=("Default", "sum"), default_rate=("Default", "mean"))
        .sort_values("default_rate", ascending=False)
    )
    out["default_rate"] = (out["default_rate"] * 100).round(3)
    return out


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    clean_path = root / "data" / "processed" / "loan_clean.csv"
    raw_path = root / "data" / "raw" / "Loan_default.csv"

    if clean_path.exists():
        df = pd.read_csv(clean_path)
        source = clean_path
    elif raw_path.exists():
        df = pd.read_csv(raw_path)
        source = raw_path
    else:
        print("Input file missing. Run Phase 5 cleaning or place raw CSV in data/raw/.")
        return

    if "Default" not in df.columns:
        raise ValueError("Expected target column 'Default' was not found.")

    df = _prepare_dataframe(df)

    fig_dir = root / "reports" / "figures" / "phase_06"
    int_dir = fig_dir / "interactive"
    fig_dir.mkdir(parents=True, exist_ok=True)
    int_dir.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    chart_rows: List[Dict[str, str]] = []

    # 1. Default class distribution
    plt.figure(figsize=(6, 4))
    sns.countplot(data=df, x="Default", hue="Default", palette="Set2", legend=False)
    plt.title("Default vs Non-Default Count")
    _safe_savefig(fig_dir / "01_default_class_distribution.png")

    # 2. Age distribution
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="Age", bins=30, kde=True, color="#2A9D8F")
    plt.title("Age Distribution")
    _safe_savefig(fig_dir / "02_age_distribution.png")

    # 3. Income distribution (log)
    plt.figure(figsize=(7, 4))
    sns.histplot(np.log1p(df["Income"]), bins=40, kde=True, color="#264653")
    plt.title("Income Distribution (log1p)")
    plt.xlabel("log1p(Income)")
    _safe_savefig(fig_dir / "03_income_distribution_log.png")

    # 4. Loan amount distribution (log)
    plt.figure(figsize=(7, 4))
    sns.histplot(np.log1p(df["LoanAmount"]), bins=40, kde=True, color="#1D3557")
    plt.title("Loan Amount Distribution (log1p)")
    plt.xlabel("log1p(LoanAmount)")
    _safe_savefig(fig_dir / "04_loanamount_distribution_log.png")

    # 5. Credit score distribution
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="CreditScore", bins=35, kde=True, color="#457B9D")
    plt.title("Credit Score Distribution")
    _safe_savefig(fig_dir / "05_creditscore_distribution.png")

    # 6. DTI distribution
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="DTIRatio", bins=35, kde=True, color="#E76F51")
    plt.title("DTI Ratio Distribution")
    _safe_savefig(fig_dir / "06_dti_distribution.png")

    # 7. Interest rate distribution
    plt.figure(figsize=(7, 4))
    sns.histplot(data=df, x="InterestRate", bins=35, kde=True, color="#F4A261")
    plt.title("Interest Rate Distribution")
    _safe_savefig(fig_dir / "07_interestrate_distribution.png")

    # 8. Loan term frequency
    plt.figure(figsize=(7, 4))
    term_counts = df["LoanTerm"].value_counts().sort_index()
    sns.barplot(x=term_counts.index, y=term_counts.values, color="#8AB17D")
    plt.title("Loan Term Frequency")
    plt.xlabel("LoanTerm")
    plt.ylabel("Count")
    _safe_savefig(fig_dir / "08_loanterm_frequency.png")

    # 9. Employment type frequency
    plt.figure(figsize=(8, 4))
    emp_counts = df["EmploymentType"].value_counts().reset_index()
    emp_counts.columns = ["EmploymentType", "count"]
    sns.barplot(data=emp_counts, x="EmploymentType", y="count", color="#9C6644")
    plt.title("Employment Type Frequency")
    plt.xticks(rotation=15)
    _safe_savefig(fig_dir / "09_employmenttype_frequency.png")

    # 10. Loan purpose frequency
    plt.figure(figsize=(8, 4))
    purpose_counts = df["LoanPurpose"].value_counts().reset_index()
    purpose_counts.columns = ["LoanPurpose", "count"]
    sns.barplot(data=purpose_counts, x="LoanPurpose", y="count", color="#6D597A")
    plt.title("Loan Purpose Frequency")
    plt.xticks(rotation=20)
    _safe_savefig(fig_dir / "10_loanpurpose_frequency.png")

    # 11. Default rate by credit score band
    rate_credit = _default_rate_by(df, "CreditScoreBand")
    plt.figure(figsize=(8, 4))
    sns.barplot(data=rate_credit, x="CreditScoreBand", y="default_rate", color="#E63946")
    plt.title("Default Rate by Credit Score Band")
    plt.ylabel("Default Rate (%)")
    _safe_savefig(fig_dir / "11_defaultrate_by_creditscoreband.png")

    # 12. Default rate by DTI band
    rate_dti = _default_rate_by(df, "DTIBand")
    plt.figure(figsize=(8, 4))
    sns.barplot(data=rate_dti, x="DTIBand", y="default_rate", color="#D62828")
    plt.title("Default Rate by DTI Band")
    plt.ylabel("Default Rate (%)")
    _safe_savefig(fig_dir / "12_defaultrate_by_dtiband.png")

    # 13. Default rate by loan purpose
    rate_purpose = _default_rate_by(df, "LoanPurpose")
    plt.figure(figsize=(9, 4))
    sns.barplot(data=rate_purpose, x="LoanPurpose", y="default_rate", color="#B56576")
    plt.title("Default Rate by Loan Purpose")
    plt.ylabel("Default Rate (%)")
    plt.xticks(rotation=20)
    _safe_savefig(fig_dir / "13_defaultrate_by_loanpurpose.png")

    # 14. Default rate by employment type
    rate_emp = _default_rate_by(df, "EmploymentType")
    plt.figure(figsize=(8, 4))
    sns.barplot(data=rate_emp, x="EmploymentType", y="default_rate", color="#7B2CBF")
    plt.title("Default Rate by Employment Type")
    plt.ylabel("Default Rate (%)")
    _safe_savefig(fig_dir / "14_defaultrate_by_employmenttype.png")

    # 15. Boxplot: Credit score by default
    plt.figure(figsize=(7, 4))
    sns.boxplot(data=df, x="Default", y="CreditScore", hue="Default", palette="Set3", legend=False)
    plt.title("Credit Score by Default Status")
    _safe_savefig(fig_dir / "15_box_creditscore_by_default.png")

    # 16. Boxplot: DTI by default
    plt.figure(figsize=(7, 4))
    sns.boxplot(data=df, x="Default", y="DTIRatio", hue="Default", palette="Set2", legend=False)
    plt.title("DTI Ratio by Default Status")
    _safe_savefig(fig_dir / "16_box_dti_by_default.png")

    # 17. Boxplot: Income by default (log)
    tmp = df.copy()
    tmp["LogIncome"] = np.log1p(tmp["Income"])
    plt.figure(figsize=(7, 4))
    sns.boxplot(data=tmp, x="Default", y="LogIncome", hue="Default", palette="Set1", legend=False)
    plt.title("Income (log1p) by Default Status")
    _safe_savefig(fig_dir / "17_box_logincome_by_default.png")

    # 18. Numeric correlation heatmap
    numeric_cols = [
        c
        for c in [
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
            "Default",
        ]
        if c in df.columns
    ]
    plt.figure(figsize=(10, 7))
    corr = df[numeric_cols].corr(numeric_only=True)
    sns.heatmap(corr, cmap="RdBu_r", center=0, annot=False)
    plt.title("Correlation Heatmap (Numeric Features)")
    _safe_savefig(fig_dir / "18_correlation_heatmap.png")

    # 19. Multivariate scatter: DTI vs CreditScore by default
    scatter_df = df.sample(min(12000, len(df)), random_state=42).copy()
    plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=scatter_df,
        x="DTIRatio",
        y="CreditScore",
        hue="Default",
        alpha=0.5,
        s=20,
        palette="Set1",
    )
    plt.title("DTI vs Credit Score by Default")
    _safe_savefig(fig_dir / "19_scatter_dti_vs_creditscore_default.png")

    # 20. Risk segment default rate
    if "RiskSegment" in df.columns:
        rate_risk = _default_rate_by(df, "RiskSegment")
        plt.figure(figsize=(8, 4))
        sns.barplot(data=rate_risk, x="RiskSegment", y="default_rate", color="#2A9D8F")
        plt.title("Default Rate by Risk Segment")
        plt.ylabel("Default Rate (%)")
        _safe_savefig(fig_dir / "20_defaultrate_by_risksegment.png")
    else:
        # Fallback chart if risk segment not available
        plt.figure(figsize=(8, 4))
        sns.scatterplot(data=scatter_df, x="InterestRate", y="DTIRatio", hue="Default", alpha=0.5, s=20)
        plt.title("Interest Rate vs DTI by Default")
        _safe_savefig(fig_dir / "20_interestrate_vs_dti_default.png")

    # Interactive plotly outputs for viva and presentation quality.
    p1 = px.scatter(
        scatter_df,
        x="DTIRatio",
        y="CreditScore",
        color="Default",
        hover_data=[c for c in ["LoanID", "LoanPurpose", "EmploymentType", "Income", "LoanAmount"] if c in scatter_df.columns],
        title="Interactive: DTI vs Credit Score by Default",
        opacity=0.55,
    )
    p1.write_html(int_dir / "interactive_dti_creditscore_default.html", include_plotlyjs="cdn")

    p2 = px.bar(
        rate_purpose,
        x="LoanPurpose",
        y="default_rate",
        title="Interactive: Default Rate by Loan Purpose",
        labels={"default_rate": "Default Rate (%)"},
    )
    p2.write_html(int_dir / "interactive_defaultrate_by_loanpurpose.html", include_plotlyjs="cdn")

    # Summary tables
    univariate_profile = pd.DataFrame(
        [
            {"metric": "row_count", "value": len(df)},
            {"metric": "default_rate_pct", "value": round(float(df["Default"].mean() * 100), 4)},
            {"metric": "avg_age", "value": round(float(df["Age"].mean()), 3)},
            {"metric": "avg_income", "value": round(float(df["Income"].mean()), 3)},
            {"metric": "avg_loan_amount", "value": round(float(df["LoanAmount"].mean()), 3)},
            {"metric": "avg_credit_score", "value": round(float(df["CreditScore"].mean()), 3)},
            {"metric": "avg_dti", "value": round(float(df["DTIRatio"].mean()), 4)},
            {"metric": "avg_interest_rate", "value": round(float(df["InterestRate"].mean()), 4)},
        ]
    )

    default_compare = df.groupby("Default", as_index=False).agg(
        loans=("Default", "size"),
        avg_income=("Income", "mean"),
        avg_loan_amount=("LoanAmount", "mean"),
        avg_credit_score=("CreditScore", "mean"),
        avg_dti=("DTIRatio", "mean"),
        avg_interest_rate=("InterestRate", "mean"),
        avg_months_employed=("MonthsEmployed", "mean"),
    )
    default_compare[[
        "avg_income",
        "avg_loan_amount",
        "avg_credit_score",
        "avg_dti",
        "avg_interest_rate",
        "avg_months_employed",
    ]] = default_compare[[
        "avg_income",
        "avg_loan_amount",
        "avg_credit_score",
        "avg_dti",
        "avg_interest_rate",
        "avg_months_employed",
    ]].round(4)

    chart_rows = [
        {"chart_no": 1, "file": "01_default_class_distribution.png", "type": "Univariate", "objective": "Assess class imbalance in target"},
        {"chart_no": 2, "file": "02_age_distribution.png", "type": "Univariate", "objective": "Age profile of borrowers"},
        {"chart_no": 3, "file": "03_income_distribution_log.png", "type": "Univariate", "objective": "Income spread and skewness"},
        {"chart_no": 4, "file": "04_loanamount_distribution_log.png", "type": "Univariate", "objective": "Loan amount spread and skewness"},
        {"chart_no": 5, "file": "05_creditscore_distribution.png", "type": "Univariate", "objective": "Credit quality distribution"},
        {"chart_no": 6, "file": "06_dti_distribution.png", "type": "Univariate", "objective": "Debt burden distribution"},
        {"chart_no": 7, "file": "07_interestrate_distribution.png", "type": "Univariate", "objective": "Pricing distribution"},
        {"chart_no": 8, "file": "08_loanterm_frequency.png", "type": "Univariate", "objective": "Term mix profile"},
        {"chart_no": 9, "file": "09_employmenttype_frequency.png", "type": "Univariate", "objective": "Employment composition"},
        {"chart_no": 10, "file": "10_loanpurpose_frequency.png", "type": "Univariate", "objective": "Purpose composition"},
        {"chart_no": 11, "file": "11_defaultrate_by_creditscoreband.png", "type": "Bivariate", "objective": "Risk by credit bucket"},
        {"chart_no": 12, "file": "12_defaultrate_by_dtiband.png", "type": "Bivariate", "objective": "Risk by DTI bucket"},
        {"chart_no": 13, "file": "13_defaultrate_by_loanpurpose.png", "type": "Bivariate", "objective": "Risk by loan purpose"},
        {"chart_no": 14, "file": "14_defaultrate_by_employmenttype.png", "type": "Bivariate", "objective": "Risk by employment type"},
        {"chart_no": 15, "file": "15_box_creditscore_by_default.png", "type": "Default Comparison", "objective": "Credit score separation by target"},
        {"chart_no": 16, "file": "16_box_dti_by_default.png", "type": "Default Comparison", "objective": "DTI separation by target"},
        {"chart_no": 17, "file": "17_box_logincome_by_default.png", "type": "Default Comparison", "objective": "Income separation by target"},
        {"chart_no": 18, "file": "18_correlation_heatmap.png", "type": "Multivariate", "objective": "Overall numeric dependency map"},
        {"chart_no": 19, "file": "19_scatter_dti_vs_creditscore_default.png", "type": "Multivariate", "objective": "Joint risk surface by target"},
        {"chart_no": 20, "file": "20_defaultrate_by_risksegment.png", "type": "Multivariate", "objective": "Composite risk segment performance"},
    ]
    chart_catalog = pd.DataFrame(chart_rows)

    univariate_out = root / "reports" / "phase_06_univariate_profile.csv"
    compare_out = root / "reports" / "phase_06_default_comparison.csv"
    catalog_out = root / "reports" / "phase_06_chart_catalog.csv"
    source_out = root / "reports" / "phase_06_source_and_outputs.md"

    univariate_profile.to_csv(univariate_out, index=False)
    default_compare.to_csv(compare_out, index=False)
    chart_catalog.to_csv(catalog_out, index=False)

    source_out.write_text(
        "\n".join(
            [
                "# Phase 6 Source and Output Log",
                f"- Data source used: `{source}`",
                f"- Chart directory: `{fig_dir}`",
                f"- Interactive chart directory: `{int_dir}`",
                f"- Static charts generated: `{len(list(fig_dir.glob('*.png'))):,}`",
                "- Summary tables:",
                f"  - `{univariate_out}`",
                f"  - `{compare_out}`",
                f"  - `{catalog_out}`",
            ]
        ),
        encoding="utf-8",
    )

    print("Phase 6 EDA completed.")
    print(f"Source: {source}")
    print(f"Charts: {fig_dir}")
    print(f"Interactive charts: {int_dir}")
    print(f"Summaries: {univariate_out}, {compare_out}, {catalog_out}")


if __name__ == "__main__":
    main()
