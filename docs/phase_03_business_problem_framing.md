# Phase 3: Business Problem Framing

## Data-Backed Context (from local audit)
- Portfolio size in dataset: **255,347** loans
- Target variable: `Default` (0/1)
- Current observed default rate: **11.613%**
- Immediate implication: roughly **1 in 9 loans** defaults, which is materially high for unsecured/retail lending portfolios.

## 1) Problem Statement
SmartCredit aims to reduce avoidable credit losses by identifying borrower and loan attributes most associated with default risk, then translating those findings into segment-level approval, pricing, and monitoring strategies.

Business problem in one line:
> The lender needs to improve approval quality by separating high-risk from low-risk applicants earlier, so default rate and portfolio loss reduce without overly shrinking good-loan growth.

## 2) Fifteen Business Questions
1. Which borrower profiles contribute the highest share of total defaults?
2. How does default rate vary across `CreditScore` bands?
3. What is the default pattern by `LoanPurpose` and which purpose is riskiest?
4. Is high `DTIRatio` consistently linked with higher default?
5. Does `Income` alone predict risk, or only when paired with `LoanAmount`?
6. Which `EmploymentType` groups show weak repayment behavior?
7. How does `MonthsEmployed` affect default odds?
8. Is there a risky interaction between low credit score and high interest rate?
9. Do co-signed loans (`HasCoSigner`) materially reduce default risk?
10. How does risk vary by `LoanTerm` (12/24/36/48/60)?
11. Which combinations of demographic + financial attributes form highest-risk segments?
12. What % of defaults come from the top-risk decile (concentration of risk)?
13. Which factors are statistically significant after controlling for other variables?
14. How much can default rate be reduced by tightening policy in top-risk bands only?
15. Which operational KPIs should risk and collections teams monitor monthly?

## 3) Stakeholders and Decision Use
- **Bank Manager (Branch / Product Owner)**:
  - Needs: approval policy thresholds, segment-wise acceptance guidance.
  - Uses output to balance disbursal growth vs risk.
- **Risk Analytics Team**:
  - Needs: statistically valid drivers, scoring logic, cut-off recommendations.
  - Uses output to refine underwriting and risk-based pricing.
- **Collections Team**:
  - Needs: early-warning risk segments and priority queues.
  - Uses output to target proactive outreach before delinquency escalation.
- **Executive Leadership (CRO / CFO / Business Head)**:
  - Needs: portfolio health trend, expected loss direction, risk-adjusted growth.
  - Uses output for strategy, capital allocation, and governance review.

## 4) Success Metrics (Phase 3 Framing Level)
### Portfolio & Risk Outcome Metrics
1. Default Rate (%) = defaults / total loans
2. Non-Default Capture (%) = good loans approved / total good loans
3. High-Risk Approval Share (%) = approved loans classified high risk / total approvals
4. Default Concentration in Top Risk Decile (%)
5. Segment Stability (month-over-month risk share drift)

### Analytical Quality Metrics
6. AUC-ROC for default discrimination
7. Recall for default class (minimizing missed defaulters)
8. Precision for high-risk flag (operational efficiency)
9. KS statistic / separation power
10. Calibration quality (predicted vs observed default)

### Business Adoption Metrics
11. Policy actions implemented from analysis (count)
12. Dashboard usage by stakeholder group (weekly views / review cadence)

## Target Direction (for capstone narrative)
- Reduce default rate from **11.613%** baseline to **<=10.2%** under simulated risk-policy scenario.
- Capture **>=60%** of defaults within top 30% predicted-risk loans.
- Maintain non-default approval capture **>=75%** to avoid over-rejecting good borrowers.

## Common Student Mistakes (Evaluator Red Flags)
1. Framing objective as "build model" instead of "improve lending decisions".
2. Asking descriptive questions only; no decision-linked questions.
3. No stakeholder mapping, so insights feel academic and not deployable.
4. Success criteria missing numeric targets.
5. No trade-off discussion (risk reduction vs business growth).

## What Faculty Usually Rewards in This Phase
- Clear business objective tied to measurable outcomes.
- Questions that map to later EDA/statistics/dashboard components.
- Stakeholder-specific interpretation (not one-size-fits-all insights).
- Realistic targets with explicit baseline reference.
