# Phase 7: Statistical Analysis

Implemented files:
- `src/statistical_analysis.py`
- `scripts/run_phase7_statistical_analysis.py`

## Scope Covered
1. Correlation analysis
2. Hypothesis testing (Welch t-test)
3. Chi-square test
4. Logistic regression significance
5. Feature importance
6. Default probability scoring

## Methods + Business Use

## 1) Correlation
- Output: `reports/phase_07_correlation_with_default.csv`
- What it does:
  - Measures linear association between numeric features and default (`Default`).
- Business use:
  - Fast shortlisting of variables for underwriting policy review.
  - Helps explain directional risk (for example, if credit score is inversely related to default).

## 2) Hypothesis Testing (Welch t-test)
- Output: `reports/phase_07_hypothesis_ttests.csv`
- What it does:
  - Compares mean of each numeric feature between defaulted and non-defaulted groups.
- Business use:
  - Provides statistical evidence for whether segment differences are real or random.
  - Supports policy arguments in review and final report.

## 3) Chi-square (Categorical vs Default)
- Output: `reports/phase_07_chi_square_results.csv`
- What it does:
  - Tests association between categorical fields (`LoanPurpose`, `EmploymentType`, etc.) and default.
  - Includes Cramer’s V effect size.
- Business use:
  - Identifies which categorical borrower segments need differential risk treatment.

## 4) Logistic Regression Significance
- Output: `reports/phase_07_logit_coefficients.csv`
- What it does:
  - Estimates multivariate default drivers with p-values and odds ratios.
- Business use:
  - Quantifies incremental effect of each feature after controlling for others.
  - Converts analytics into policy thresholds and risk-pricing logic.

## 5) Feature Importance
- Output: `reports/phase_07_feature_importance.csv`
- What it does:
  - Ranks features by absolute logistic coefficient magnitude (standardized modeling flow).
- Business use:
  - Prioritizes the top few levers to monitor in dashboard and operational scorecards.

## 6) Default Probability Scoring
- Output: `data/processed/phase_07_default_probability_scores.csv`
- What it does:
  - Produces borrower-level default probabilities and 5 risk bands.
- Business use:
  - Enables risk-based approval cutoffs.
  - Enables collections prioritization (high probability first).

## Model Performance Output
- Output: `reports/phase_07_model_performance.csv`
- Includes:
  - ROC-AUC
  - PR-AUC
  - Train/Test row counts

## Execution
```bash
python scripts/run_phase7_statistical_analysis.py
```

## Common Student Mistakes (Strict Evaluator Red Flags)
1. Reporting significance without effect size or business interpretation.
2. Using only univariate tests and ignoring multivariate control.
3. Treating p-value as business impact size.
4. Reporting accuracy only for imbalanced default data.
5. Not exporting scored probabilities for downstream KPI/dashboard usage.
