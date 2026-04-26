# SmartCredit: Loan Default Analytics for Better Lending Decisions

A finance analytics capstone project that analyzes borrower behavior, quantifies default drivers, and converts findings into actionable lending strategy.

## Problem Statement
Lenders need to reduce avoidable defaults while preserving healthy loan growth. This project builds a full analytics workflow from ETL and cleaning to EDA, statistical validation, risk scoring, KPI framework, and Tableau storytelling.

## Dataset
- Source: [Kaggle Loan Default Dataset](https://www.kaggle.com/datasets/nikhil1e9/loan-default)
- Local expected path: `data/raw/Loan_default.csv`
- Shape observed in local audit: `255,347 rows x 18 columns`
- Target variable: `Default` (`1=Default`, `0=Non-Default`)

## Objectives
1. Identify key drivers of default risk.
2. Build borrower-level probability scoring.
3. Create business KPIs for underwriting and collections.
4. Design Tableau dashboards for executive decision-making.

## Repository Structure
```text
loan_default/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_import_and_audit.ipynb
│   ├── 02_cleaning_pipeline.ipynb
│   ├── 03_eda.ipynb
│   ├── 04_statistical_analysis.ipynb
│   ├── 05_feature_engineering.ipynb
│   └── 06_kpi_export.ipynb
├── scripts/
│   ├── phase2_profile_dataset.py
│   ├── run_phase5_cleaning.py
│   ├── run_phase6_eda.py
│   ├── run_phase7_statistical_analysis.py
│   └── run_phase8_kpi_framework.py
├── src/
│   ├── cleaning_pipeline.py
│   └── statistical_analysis.py
├── tableau/
│   ├── dashboard_blueprint.csv
│   └── screenshots/
├── docs/
├── reports/
├── requirements.txt
└── README.md
```

## Tech Stack
- Python: `pandas`, `numpy`, `scipy`, `statsmodels`, `scikit-learn`
- Visualization: `matplotlib`, `seaborn`, `plotly`
- BI: Tableau
- Version Control: Git + GitHub

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Execution Workflow
1. Place dataset in `data/raw/Loan_default.csv`.
2. Profile schema:
```bash
python scripts/phase2_profile_dataset.py
```
3. Clean data:
```bash
python scripts/run_phase5_cleaning.py
```
4. Generate EDA visuals:
```bash
python scripts/run_phase6_eda.py
```
5. Run statistical analysis:
```bash
python scripts/run_phase7_statistical_analysis.py
```
6. Generate KPI scorecard:
```bash
python scripts/run_phase8_kpi_framework.py
```

## Key Output Artifacts
- Cleaning outputs: `data/processed/loan_clean.csv`
- EDA charts: `reports/figures/phase_06/`
- Statistical outputs: `reports/phase_07_*.csv`
- Probability scores: `data/processed/phase_07_default_probability_scores.csv`
- KPI values: `data/processed/phase_08_kpi_values.csv`
- Tableau blueprint: `tableau/dashboard_blueprint.csv`

## Dashboard Story (Tableau)
1. Executive Summary
2. Customer Risk Segments
3. Loan Performance
4. Demographic Insights

Screenshot checklist is maintained in `tableau/screenshots/README.md`.

## Business Value
- Improves approval quality through risk segmentation.
- Helps reduce bad-debt exposure with early warning signals.
- Supports collections prioritization using default probability scores.
- Provides governance-ready KPI tracking for monthly reviews.

## Evaluation-Ready Practices
- Phase-wise artifacts and reproducible scripts
- Statistical significance + effect evidence
- Business-linked recommendations with measurable impact
- Documentation for final report and presentation

## Team Collaboration (Suggested)
- Work via feature branches and reviewed pull requests.
- Keep commits scoped, descriptive, and reproducible.
- Record outputs and assumptions in `docs/` and `reports/`.

## Disclaimer
This project is for academic and analytical purposes. It should not be used as a production lending decision engine without regulatory, fairness, and governance validation.
