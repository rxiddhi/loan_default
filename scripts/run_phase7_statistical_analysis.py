"""Run Phase 7 statistical analysis and export outputs.

Usage:
    python scripts/run_phase7_statistical_analysis.py
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.statistical_analysis import run_full_statistical_analysis


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
        print("No input found. Provide data/raw/Loan_default.csv or run Phase 5 first.")
        return

    outputs = run_full_statistical_analysis(df)

    reports_dir = root / "reports"
    proc_dir = root / "data" / "processed"
    reports_dir.mkdir(parents=True, exist_ok=True)
    proc_dir.mkdir(parents=True, exist_ok=True)

    out_corr = reports_dir / "phase_07_correlation_with_default.csv"
    out_ttest = reports_dir / "phase_07_hypothesis_ttests.csv"
    out_chi = reports_dir / "phase_07_chi_square_results.csv"
    out_logit = reports_dir / "phase_07_logit_coefficients.csv"
    out_imp = reports_dir / "phase_07_feature_importance.csv"
    out_perf = reports_dir / "phase_07_model_performance.csv"
    out_scores = proc_dir / "phase_07_default_probability_scores.csv"
    out_summary = reports_dir / "phase_07_source_and_outputs.md"

    outputs.correlation_df.to_csv(out_corr, index=False)
    outputs.ttest_df.to_csv(out_ttest, index=False)
    outputs.chi_square_df.to_csv(out_chi, index=False)
    outputs.logit_coef_df.to_csv(out_logit, index=False)
    outputs.feature_importance_df.to_csv(out_imp, index=False)
    outputs.model_perf_df.to_csv(out_perf, index=False)
    outputs.scored_df.to_csv(out_scores, index=False)

    out_summary.write_text(
        "\n".join(
            [
                "# Phase 7 Statistical Analysis Log",
                f"- Source used: `{source}`",
                f"- Rows analyzed: `{len(df):,}`",
                f"- Correlation output: `{out_corr}`",
                f"- Hypothesis test output: `{out_ttest}`",
                f"- Chi-square output: `{out_chi}`",
                f"- Logistic significance output: `{out_logit}`",
                f"- Feature importance output: `{out_imp}`",
                f"- Model performance output: `{out_perf}`",
                f"- Probability scores output: `{out_scores}`",
            ]
        ),
        encoding="utf-8",
    )

    print("Phase 7 completed.")
    print(f"Source: {source}")
    print(f"Saved: {out_corr}")
    print(f"Saved: {out_ttest}")
    print(f"Saved: {out_chi}")
    print(f"Saved: {out_logit}")
    print(f"Saved: {out_imp}")
    print(f"Saved: {out_perf}")
    print(f"Saved: {out_scores}")


if __name__ == "__main__":
    main()
