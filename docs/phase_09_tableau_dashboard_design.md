# Phase 9: Tableau Dashboard Design (4-Dashboard Story)

## Dashboard 1: Executive Summary
- Layout:
  - Top row KPI tiles: Total Loans, Default Rate, Avg Loan Size, Portfolio Health Score.
  - Mid row: default trend and segment risk snapshot.
  - Bottom row: top risky purpose and employment segments.
- Charts:
  - KPI cards, bullet chart, bar chart, line chart.
- Filters:
  - LoanPurpose, EmploymentType, LoanTerm, CreditScoreBand.
- Interactions:
  - Click segment bar to cross-filter all charts.
- Color theme:
  - Healthy: `#2A9D8F`, Warning: `#F4A261`, Risk: `#E63946`, Neutral: `#264653`.
- Story logic:
  - Start with portfolio health, then zoom to risk concentration drivers.
- Screenshot name:
  - `dashboard_01_executive_summary.png`

## Dashboard 2: Customer Risk Segments
- Layout:
  - Left: risk-segment distribution.
  - Center: probability band vs actual default rate.
  - Right: borrower profile table for high-risk segment.
- Charts:
  - Stacked bar, heatmap, scatter, detail table.
- Filters:
  - RiskBand, CreditScoreBand, DTIBand, HasCoSigner.
- Interactions:
  - Click risk band -> highlight segment profile and default mix.
- Color theme:
  - Gradient green to red by risk intensity.
- Story logic:
  - Explain who is risky and why the segment is risky.
- Screenshot name:
  - `dashboard_02_customer_risk_segments.png`

## Dashboard 3: Loan Performance
- Layout:
  - Top: portfolio mix by purpose and term.
  - Mid: default rate by purpose and interest-rate bucket.
  - Bottom: exposure-risk matrix.
- Charts:
  - Treemap, clustered bar, matrix heatmap.
- Filters:
  - LoanPurpose, LoanTerm, InterestRate bucket, Income band.
- Interactions:
  - Hover on matrix cell shows exposure + default + avg score.
- Color theme:
  - Blues for exposure, reds for risk overlay.
- Story logic:
  - Show where portfolio volume overlaps with high risk.
- Screenshot name:
  - `dashboard_03_loan_performance.png`

## Dashboard 4: Demographic Insights
- Layout:
  - Top: demographic mix.
  - Mid: default by marital status, education, and dependents.
  - Bottom: age x income risk map.
- Charts:
  - Mosaic/stacked bars, boxplots, bubble chart.
- Filters:
  - Age band, MaritalStatus, Education, HasDependents.
- Interactions:
  - Select demographic cluster to update default and capacity metrics.
- Color theme:
  - Neutral categorical palette with red overlay for risk.
- Story logic:
  - Convert demographic patterns into policy-safe insights.
- Screenshot name:
  - `dashboard_04_demographic_insights.png`

## Tableau Assets to Save in Repo
- `tableau/screenshots/dashboard_01_executive_summary.png`
- `tableau/screenshots/dashboard_02_customer_risk_segments.png`
- `tableau/screenshots/dashboard_03_loan_performance.png`
- `tableau/screenshots/dashboard_04_demographic_insights.png`
- `tableau/screenshots/dashboard_00_storyboard_overview.png`

## Common Student Mistakes
1. Dashboard has many charts but no narrative flow.
2. No cross-filter actions; static visuals only.
3. Weak color semantics (risk not visually obvious).
4. No clear executive summary tile row.
