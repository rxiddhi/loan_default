# Phase 8: KPI Framework

Implemented files:
- `reports/phase_08_kpi_definitions.csv`
- `scripts/run_phase8_kpi_framework.py`

Run:
```bash
python scripts/run_phase8_kpi_framework.py
```

Generated outputs:
- `data/processed/phase_08_kpi_values.csv`
- `data/processed/phase_08_portfolio_health_score.csv`
- `reports/phase_08_kpi_scorecard.md`

## KPI Buckets
1. Portfolio risk and quality
2. Underwriting stability and affordability
3. Segment-level risk concentration
4. Collections and recovery opportunity
5. Model-risk capture and early warning

## Evaluator Notes
- This framework includes 20 KPI definitions with formulas and owners.
- KPIs are dashboard-ready and mapped to business functions.
- Includes a custom `Portfolio Health Score` for executive communication.

## Common Mistakes to Avoid
1. Showing KPIs without formulas.
2. Using only overall averages with no segment risk KPIs.
3. No ownership mapping, making KPIs operationally weak.
