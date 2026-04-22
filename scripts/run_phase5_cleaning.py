"""Run Phase 5 cleaning pipeline as a standalone ETL step.

Usage:
    python scripts/run_phase5_cleaning.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.cleaning_pipeline import CleaningConfig, clean_loan_data


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    raw_path = root / "data" / "raw" / "Loan_default.csv"
    clean_out = root / "data" / "processed" / "loan_clean.csv"
    summary_out = root / "data" / "processed" / "phase_05_cleaning_summary.csv"
    profile_out = root / "data" / "processed" / "phase_05_missing_profile.csv"

    if not raw_path.exists():
        print(f"Input file not found: {raw_path}")
        print("Place Kaggle CSV at data/raw/Loan_default.csv and rerun.")
        return

    df = pd.read_csv(raw_path)
    cleaned, summary = clean_loan_data(
        df,
        CleaningConfig(
            enforce_numeric_bounds=True,
            cap_outliers_iqr=True,
            iqr_multiplier=1.5,
            create_missing_indicators=True,
            encode_binary_flags=True,
        ),
    )

    clean_out.parent.mkdir(parents=True, exist_ok=True)
    cleaned.to_csv(clean_out, index=False)
    summary.to_csv(summary_out, index=False)

    missing_profile = pd.DataFrame(
        {
            "column": cleaned.columns,
            "missing_count": cleaned.isna().sum().values,
            "missing_pct": (cleaned.isna().mean() * 100).round(4).values,
            "dtype": [str(t) for t in cleaned.dtypes],
        }
    )
    missing_profile.to_csv(profile_out, index=False)

    print("Phase 5 cleaning completed.")
    print(f"Saved cleaned file: {clean_out}")
    print(f"Saved summary: {summary_out}")
    print(f"Saved missing profile: {profile_out}")


if __name__ == "__main__":
    main()
