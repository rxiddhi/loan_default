# Phase 4: Python ETL Notebook Workflow

This workflow is designed for evaluator-visible rigor: each notebook has a single responsibility, tangible outputs, and commit-level traceability.

## 1) `01_import_and_audit.ipynb`
- Purpose: Ingest raw CSV, validate schema integrity, and generate baseline audit artifacts.
- Sections:
  1. Setup and path config
  2. Load raw dataset
  3. Structural checks (shape, duplicates, target ratio)
  4. Column-level quality profile
  5. Export audit outputs
- Core code cells:
  1. Import `pandas/numpy/pathlib`
  2. `pd.read_csv()` for raw input
  3. Duplicate and default-rate checks
  4. Missingness + uniqueness profile table
  5. Export `01_column_profile.csv` and markdown summary
- Outputs:
  - `data/processed/01_column_profile.csv`
  - `docs/phase_04_audit_summary.md`
- What to commit:
  - Notebook file
  - Exported audit profile and summary

## 2) `02_cleaning_pipeline.ipynb`
- Purpose: Produce consistent, analysis-ready dataset with transparent cleaning log.
- Sections:
  1. Load and deduplicate
  2. String standardization
  3. Numeric type casting
  4. Missing-value treatment
  5. Feature additions for risk segmentation
  6. Export cleaned table + cleaning log
- Core code cells:
  1. Dedup logic
  2. Category normalize (`strip/title`)
  3. Type coercion with `errors='coerce'`
  4. Median/mode-like fills
  5. Derived features (`IncomeToLoanRatio`, `CreditScoreBand`, `DTIBand`)
  6. Export `loan_clean.csv`, `02_cleaning_log.csv`
- Outputs:
  - `data/processed/loan_clean.csv`
  - `data/processed/02_cleaning_log.csv`
- What to commit:
  - Notebook + cleaned data schema evidence (not raw data dump if policy disallows)

## 3) `03_eda.ipynb`
- Purpose: Identify high-risk patterns through descriptive analytics and visual evidence.
- Sections:
  1. Load cleaned data
  2. Univariate distributions
  3. Default vs non-default comparisons
  4. Segment summaries
  5. Visual export for report/Tableau story
- Core code cells:
  1. `seaborn/matplotlib/plotly` setup
  2. Default class distribution chart
  3. Credit score vs default chart
  4. Purpose-level default summary table
  5. DTI vs Credit scatter (sampled)
- Outputs:
  - `reports/figures/eda_default_distribution.png`
  - `reports/figures/eda_creditscore_vs_default.png`
  - `reports/phase_04_eda_summary.csv`
- What to commit:
  - Notebook + plot images + summary CSV

## 4) `04_statistical_analysis.ipynb`
- Purpose: Statistically validate observed EDA relationships.
- Sections:
  1. Load cleaned data
  2. Chi-square for categorical variables
  3. Numeric mean-difference test (t-test)
  4. Logistic regression significance table
  5. Export inferential outputs
- Core code cells:
  1. `chi2_contingency` loop for categoricals
  2. Welch t-test (`InterestRate` by default class)
  3. `statsmodels.Logit` estimation
  4. Coefficient and p-value export
- Outputs:
  - `reports/phase_04_chi_square_results.csv`
  - `reports/phase_04_logit_coefficients.csv`
- What to commit:
  - Notebook + statistical output tables

## 5) `05_feature_engineering.ipynb`
- Purpose: Create predictive features and baseline default scoring outputs.
- Sections:
  1. Additional feature derivation
  2. Encoding and train-test split
  3. Baseline logistic model
  4. Feature-strength extraction
  5. Default probability and risk banding
- Core code cells:
  1. Derived features (`LoanToIncome`, `RateXDTI`, `IsThinFile`)
  2. One-hot encoding + stratified split
  3. Logistic regression fit + AUC
  4. Coefficient magnitude ranking
  5. Score export with risk bands
- Outputs:
  - `data/processed/05_feature_matrix.parquet`
  - `data/processed/05_default_scored.csv`
  - `reports/phase_05_feature_strength.csv`
- What to commit:
  - Notebook + modeling outputs (if size reasonable)

## 6) `06_kpi_export.ipynb`
- Purpose: Create executive/operational KPI tables and Tableau-ready extract.
- Sections:
  1. Portfolio-level KPI build
  2. Segment-level KPI build
  3. Join scored probabilities (if available)
  4. Tableau extract generation
- Core code cells:
  1. KPI master table creation
  2. Employment x Purpose segment metrics
  3. Output for Tableau ingestion
- Outputs:
  - `data/processed/kpi_master.csv`
  - `data/processed/kpi_segment_table.csv`
  - `data/processed/tableau_input.csv`
- What to commit:
  - Notebook + KPI exports + schema note in docs if changed

## Recommended Commit Sequence for Phase 4
1. `feat(notebooks): scaffold six-step ETL and analytics workflow notebooks`
2. `docs: add phase 4 notebook execution guide and expected artifacts`
3. `chore: add figures output directory scaffold`

## Common Student Mistakes in Phase 4
1. Mixing cleaning, EDA, and modeling in one notebook (poor traceability).
2. No export artifacts, so work cannot be validated by evaluator.
3. Hard-coded local paths that break on another machine.
4. Ignoring reproducibility (missing seeds, no deterministic sampling).
5. Overwriting outputs without a documented workflow.
