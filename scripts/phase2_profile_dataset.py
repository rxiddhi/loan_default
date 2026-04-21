"""Phase 2 dataset profiling for SmartCredit.

Usage:
    python scripts/phase2_profile_dataset.py

Expected input:
    data/raw/Loan_default.csv

Outputs:
    docs/phase_02_observed_schema.md
    data/processed/phase_02_column_profile.csv
"""

from __future__ import annotations

from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_PATH = BASE_DIR / "data" / "raw" / "Loan_default.csv"
SCHEMA_OUT = BASE_DIR / "docs" / "phase_02_observed_schema.md"
PROFILE_OUT = BASE_DIR / "data" / "processed" / "phase_02_column_profile.csv"

EXPECTED_COLUMNS = [
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


def main() -> None:
    if not RAW_PATH.exists():
        print(f"Input file not found: {RAW_PATH}")
        print("Place the Kaggle CSV at data/raw/Loan_default.csv and re-run.")
        return

    df = pd.read_csv(RAW_PATH)

    col_profile = pd.DataFrame(
        {
            "column": df.columns,
            "dtype": [str(t) for t in df.dtypes],
            "missing_count": df.isna().sum().values,
            "missing_pct": (df.isna().mean() * 100).round(4).values,
            "unique_count": [df[c].nunique(dropna=True) for c in df.columns],
        }
    )
    PROFILE_OUT.parent.mkdir(parents=True, exist_ok=True)
    col_profile.to_csv(PROFILE_OUT, index=False)

    missing_expected = [c for c in EXPECTED_COLUMNS if c not in df.columns]
    unexpected_cols = [c for c in df.columns if c not in EXPECTED_COLUMNS]
    dup_rows = int(df.duplicated().sum())
    dup_loan_ids = int(df["LoanID"].duplicated().sum()) if "LoanID" in df.columns else -1
    default_rate = (
        float(df["Default"].mean()) * 100
        if "Default" in df.columns and pd.api.types.is_numeric_dtype(df["Default"])
        else float("nan")
    )

    lines = [
        "# Phase 2 Observed Schema Audit",
        "",
        f"- File: `{RAW_PATH}`",
        f"- Rows: `{len(df):,}`",
        f"- Columns: `{df.shape[1]}`",
        f"- Duplicate rows: `{dup_rows}`",
        f"- Duplicate LoanID: `{dup_loan_ids}`",
        f"- Default rate (%): `{default_rate:.3f}`" if default_rate == default_rate else "- Default rate (%): `N/A`",
        "",
        "## Schema Validation",
        f"- Missing expected columns: `{missing_expected}`",
        f"- Unexpected columns: `{unexpected_cols}`",
        "",
        "## Column Dtypes",
    ]

    for _, row in col_profile.iterrows():
        lines.append(
            f"- `{row['column']}`: dtype={row['dtype']}, missing={int(row['missing_count'])} ({row['missing_pct']}%), unique={int(row['unique_count'])}"
        )

    SCHEMA_OUT.write_text("\n".join(lines), encoding="utf-8")

    print("Phase 2 profiling completed.")
    print(f"Saved: {PROFILE_OUT}")
    print(f"Saved: {SCHEMA_OUT}")


if __name__ == "__main__":
    main()
