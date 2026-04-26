# Phase 6: EDA + Visual Analysis

This phase translates cleaned loan data into risk insights using:
- `pandas`, `numpy`
- `matplotlib`, `seaborn`
- `plotly`

Implemented script:
- `scripts/run_phase6_eda.py`

Primary output folder:
- `reports/figures/phase_06/`

## 1) Univariate Analysis (What each variable looks like)
Focus areas:
1. Target distribution (`Default`) to quantify class imbalance.
2. Numeric distributions: `Age`, `Income`, `LoanAmount`, `CreditScore`, `DTIRatio`, `InterestRate`.
3. Categorical composition: `EmploymentType`, `LoanPurpose`, `LoanTerm`.

Business use:
- Understand base population mix before claiming risk patterns.

## 2) Bivariate Analysis (Feature vs Default)
Focus areas:
1. Default rate by `CreditScoreBand`.
2. Default rate by `DTIBand`.
3. Default rate by `LoanPurpose`.
4. Default rate by `EmploymentType`.

Business use:
- Identifies where underwriting policy should tighten or monitor more closely.

## 3) Multivariate Analysis (Combined risk effects)
Focus areas:
1. Correlation heatmap of numeric drivers.
2. DTI vs CreditScore scatter colored by default class.
3. Composite `RiskSegment` default behavior.

Business use:
- Finds interaction risk not visible in one-variable analysis.

## 4) Default vs Non-Default Comparison
Comparative table exported to:
- `reports/phase_06_default_comparison.csv`

Includes side-by-side means for:
- Income
- LoanAmount
- CreditScore
- DTIRatio
- InterestRate
- MonthsEmployed

Business use:
- Supports presentation narrative with concrete numeric separation between classes.

## 5) Twenty Best Charts (Portfolio-Quality Set)
Generated catalog:
- `reports/phase_06_chart_catalog.csv`

Chart set:
1. Default class distribution
2. Age distribution
3. Income distribution (log)
4. Loan amount distribution (log)
5. Credit score distribution
6. DTI distribution
7. Interest rate distribution
8. Loan term frequency
9. Employment type frequency
10. Loan purpose frequency
11. Default rate by credit score band
12. Default rate by DTI band
13. Default rate by loan purpose
14. Default rate by employment type
15. Credit score boxplot by default
16. DTI boxplot by default
17. Log-income boxplot by default
18. Correlation heatmap
19. DTI vs credit score scatter by default
20. Default rate by risk segment

Interactive (Plotly) visuals:
- `interactive_dti_creditscore_default.html`
- `interactive_defaultrate_by_loanpurpose.html`

## 6) Expected Insights (Realistic)
1. Default class is minority but materially significant.
2. Lower credit score bands should show higher default rates.
3. Higher DTI bands should show elevated default behavior.
4. Some loan purposes likely concentrate higher risk.
5. Defaulters typically show weaker credit profile and higher pricing pressure.
6. Composite risk segmentation should show monotonic risk escalation from low to very high risk.

## Execution
```bash
python scripts/run_phase6_eda.py
```

## Common Student Mistakes (Strict Evaluator Red Flags)
1. Showing only generic plots with no default-focus comparison.
2. Using counts where rates are required (misleading risk inference).
3. Ignoring class imbalance in interpretation.
4. Presenting correlation as causation.
5. No exported chart files or catalog (hard to evaluate reproducibility).
