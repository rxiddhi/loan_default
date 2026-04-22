# Phase 5: Robust Data Cleaning Strategy

This phase converts raw loan records into an analysis-grade dataset with auditable transformations suitable for capstone evaluation and portfolio use.

## Cleaning Objective
Build a deterministic cleaning pipeline that is:
- **repeatable** (same outputs for same inputs),
- **traceable** (every major action logged),
- **business-safe** (no unrealistic data leakage),
- **analytics-ready** (usable for EDA, stats, modeling, Tableau).

## Implemented Assets
- Pipeline module: `src/cleaning_pipeline.py`
- Runner script: `scripts/run_phase5_cleaning.py`
- Primary output: `data/processed/loan_clean.csv`
- Audit outputs:
  - `data/processed/phase_05_cleaning_summary.csv`
  - `data/processed/phase_05_missing_profile.csv`

## 1) Missing Values
Strategy:
- Numeric fields: median imputation.
- Categorical fields: mode imputation (fallback `Unknown`).
- Missing indicators: create `<column>_was_missing` flags to preserve information.

Why evaluator-friendly:
- Prevents silent data loss from row drops.
- Maintains transparency of originally incomplete records.

## 2) Duplicates
Strategy:
- Remove exact duplicate rows first.
- Track duplicate counts pre/post in summary.
- Monitor `LoanID` duplication separately in audit metrics.

Why evaluator-friendly:
- Distinguishes row-level duplication vs key-level integrity issues.

## 3) Outliers
Strategy:
- Domain bound checks convert impossible values to null first.
- IQR capping (`1.5 * IQR`) for heavy-tail numeric fields:
  - `Income`, `LoanAmount`, `InterestRate`, `DTIRatio`, `LoanToIncomeRatio`

Why evaluator-friendly:
- Keeps all observations while reducing distortion in mean-based metrics and regression coefficients.

## 4) Incorrect Datatypes
Strategy:
- Explicit numeric coercion with `errors='coerce'`.
- Explicit categorical standardization for string fields.

Why evaluator-friendly:
- Prevents hidden object-type issues breaking stats/modeling downstream.

## 5) Standardization
Strategy:
- Strip whitespace and title-case category labels.
- Normalize yes/no variants (`Y`, `True`, `1` -> `Yes`; `N`, `False`, `0` -> `No`).

Why evaluator-friendly:
- Avoids fragmented groupings in pivot tables and charts.

## 6) Encoding
Strategy:
- Keep original categorical columns for interpretability.
- Add binary flag columns for yes/no features:
  - `HasMortgage_Flag`
  - `HasDependents_Flag`
  - `HasCoSigner_Flag`

Why evaluator-friendly:
- Supports both business-readable dashboards and model-ready numeric features.

## 7) Feature Engineering
Implemented engineered columns:
- `IncomeToLoanRatio`
- `LoanToIncomeRatio`
- `RateXDTI`
- `CreditScoreBand`
- `DTIBand`
- `LTI_Band`

Why these matter:
- Capture affordability, leverage pressure, and combined risk intensity.

## 8) Risk Segmentation Columns
Implemented risk segmentation:
- `RiskPoints` (composite from credit, DTI, and LTI bands)
- `RiskSegment` with 4 levels:
  - `Low Risk`
  - `Moderate Risk`
  - `High Risk`
  - `Very High Risk`

Business value:
- Directly usable by underwriting and collections for policy and prioritization.

## Execution
```bash
python scripts/run_phase5_cleaning.py
```

## Common Student Mistakes (Strict Evaluator Red Flags)
1. Dropping all rows with any nulls (unnecessary data loss).
2. Outlier deletion without justification.
3. Encoding categories too early and losing interpretability.
4. No before/after cleaning summary artifacts.
5. No risk segmentation fields despite a lending use case.

## Quality Check Before Phase 6
1. Verify `loan_clean.csv` exists and opens without dtype warnings.
2. Ensure `phase_05_cleaning_summary.csv` shows reduced anomalies.
3. Validate `RiskSegment` distribution is not degenerate (single class).
