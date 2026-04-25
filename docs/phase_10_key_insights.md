# Phase 10: Key Insights (Data-Backed)

Baseline source:
- `reports/phase_06_univariate_profile.csv`
- `reports/phase_06_default_comparison.csv`

## 12 Insights
1. Portfolio default rate is **11.6128%** over **255,347** loans, indicating meaningful credit-risk pressure.
2. Defaulters have **14.37% lower average income** (`71,844.72`) vs non-defaulters (`83,899.17`), suggesting weaker repayment capacity.
3. Defaulters carry **15.29% higher average loan amount** (`144,515.31`) vs non-defaulters (`125,353.66`), increasing loss exposure per risky account.
4. Average credit score is lower in default group by **16.95 points** (`559.29` vs `576.23`), confirming bureau score as a strong risk discriminator.
5. Average interest rate for defaulters is **2.7192 percentage points higher** (`15.8962` vs `13.177`), showing risk-based pricing alone is not offsetting losses.
6. Defaulters have shorter employment history by **10.53 months** (`50.24` vs `60.76`), indicating stability risk.
7. Defaulter DTI is higher (`0.5125`) than non-defaulter DTI (`0.4986`), supporting debt burden as a directional risk driver.
8. Portfolio-wide average credit score (`574.264`) sits near the lower scoring tiers, meaning the book is structurally moderate-to-high risk.
9. Portfolio average DTI (`0.5002`) is high, indicating thin affordability buffers across a large borrower base.
10. Average loan size (`127,578.87`) exceeds average annual income (`82,499.31`) by a wide margin, implying leverage-heavy underwriting.
11. Class imbalance exists (about **1 default : 7.6 non-defaults**), so model evaluation must prioritize recall/precision and PR-AUC over plain accuracy.
12. Risk-stratified dashboards are essential: aggregate KPIs alone can hide high-risk pockets in purpose/employment segments.
