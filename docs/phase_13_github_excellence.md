# Phase 13: GitHub Excellence Plan

## 1) Realistic 18-Commit Timeline (Back-commit Friendly)
1. `chore: initialize repo scaffold and folder taxonomy`
2. `build: add python requirements and gitignore`
3. `docs: add project overview and objective framing`
4. `docs: add dataset understanding and target definition`
5. `feat: add schema profiling script`
6. `docs: add business problem framing and stakeholder map`
7. `feat: scaffold six-notebook ETL workflow`
8. `docs: add notebook execution guide and output contract`
9. `feat: implement reusable cleaning pipeline module`
10. `feat: add phase 5 cleaning runner and logs`
11. `feat: add phase 6 EDA visual pipeline with chart exports`
12. `docs: add EDA insight guide and chart catalog`
13. `feat: add statistical analysis module and runner`
14. `docs: add phase 7 statistical interpretation`
15. `feat: add KPI framework generator and scorecard exports`
16. `docs: add Tableau dashboard blueprint`
17. `docs: add final report and internship packaging`
18. `docs: publish professional README and project governance`

## 2) Branch Strategy for 5 Members
- `main`: protected release branch.
- `dev`: integration branch.
- `feature/member1-etl`
- `feature/member2-eda`
- `feature/member3-stats`
- `feature/member4-tableau`
- `feature/member5-docs-presentation`

Rules:
- No direct push to `main`.
- PR to `dev` first, then release PR to `main`.
- Keep PR size under ~400 lines where possible.

## 3) PR Workflow
1. Pull latest `dev`.
2. Create feature branch.
3. Push focused commit set.
4. Open PR with template:
- objective
- files changed
- test evidence
- screenshots/output proof
5. Minimum 1 peer review approval.
6. Squash merge only when linear history is preferred.

## 4) What Faculty Checks in GitHub Insights
1. Commit consistency over time (not one-day dump).
2. Multiple contributors and fair activity split.
3. Meaningful commit messages.
4. PR reviews and discussion quality.
5. Evidence files (outputs, docs, screenshots) and reproducibility.

## 5) How to Look Professional
1. Use deterministic file naming across phases.
2. Keep docs synchronized with code outputs.
3. Add issue labels (`etl`, `eda`, `stats`, `tableau`, `docs`).
4. Include dashboard screenshots and clear changelog.
5. Keep README actionable with setup + outcomes + artifacts.
