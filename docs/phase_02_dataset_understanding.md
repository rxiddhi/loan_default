# Phase 2: Dataset Understanding (SmartCredit)

## Scope
Dataset expected: `data/raw/Loan_default.csv` from Kaggle `nikhil1e9/loan-default`.

This phase documents the expected schema and business interpretation before ETL. Run the profiling script in `scripts/phase2_profile_dataset.py` immediately after placing the CSV to confirm assumptions.

## 1) Likely Columns (18)
1. LoanID
2. Age
3. Income
4. LoanAmount
5. CreditScore
6. MonthsEmployed
7. NumCreditLines
8. InterestRate
9. LoanTerm
10. DTIRatio
11. Education
12. EmploymentType
13. MaritalStatus
14. HasMortgage
15. HasDependents
16. LoanPurpose
17. HasCoSigner
18. Default

## 2) Target Variable
- `Default` (binary):
  - `1` = borrower defaulted
  - `0` = borrower did not default

## 3) Business Meaning by Column
| Column | Type (Expected) | Business Meaning |
|---|---|---|
| LoanID | string | Unique loan application identifier (not predictive by itself). |
| Age | int | Borrower life-stage proxy; may relate to repayment stability. |
| Income | int | Core repayment capacity signal. |
| LoanAmount | int | Exposure size; larger amounts can increase expected loss. |
| CreditScore | int | Creditworthiness proxy from bureau behavior. |
| MonthsEmployed | int | Employment stability indicator. |
| NumCreditLines | int | Existing credit footprint / leverage behavior. |
| InterestRate | float | Risk-based pricing signal; often higher for riskier borrowers. |
| LoanTerm | int | Repayment tenure; longer terms can alter risk profile. |
| DTIRatio | float | Debt burden relative to income; high values usually elevate risk. |
| Education | category | Socio-economic segmentation feature. |
| EmploymentType | category | Income stability proxy (e.g., full-time vs unemployed). |
| MaritalStatus | category | Household profile segmentation. |
| HasMortgage | category (Yes/No) | Existing debt commitment indicator. |
| HasDependents | category (Yes/No) | Household expense pressure proxy. |
| LoanPurpose | category | Risk differs by use-case (business/home/auto/etc.). |
| HasCoSigner | category (Yes/No) | Secondary repayment support indicator. |
| Default | int (0/1) | Loan performance outcome (target). |

## 4) Likely Risk Indicators
- High `DTIRatio`
- Low `CreditScore`
- Low `Income` relative to `LoanAmount`
- High `InterestRate` (risk-priced accounts)
- Lower `MonthsEmployed` (unstable income history)
- Certain `EmploymentType` categories (e.g., unemployed/part-time)
- Certain `LoanPurpose` segments (portfolio dependent)
- No co-signer for marginal profiles

## 5) Data Quality Issues to Expect
- `LoanID` uniqueness violations (duplicate keys)
- Categorical casing inconsistencies (`yes` vs `Yes`)
- Hidden whitespace in object columns
- Out-of-range numeric values (e.g., DTI outside expected range)
- Data type drift after CSV load (numbers parsed as strings)
- Class imbalance in `Default` (typically minority class = default)
- Potential leakage if engineered fields accidentally use target logic

## 6) Initial Observations (Pre-ETL)
- Dataset is widely reported as ~255k rows and 18 columns.
- Mixed data types (numeric + categorical) are suitable for risk segmentation and classification.
- `Default` is binary, so KPI design should always include class-imbalance awareness.
- Features already align strongly with underwriting workflows (capacity, stability, leverage, and purpose).

## Common Student Mistakes (Evaluator Red Flags)
1. Treating `LoanID` as a predictive feature.
2. Running models before schema validation and data-type correction.
3. Ignoring imbalance and reporting only accuracy.
4. Not documenting assumptions around category standardization.
5. Mixing business interpretation and causal claims without statistical testing.

## Immediate Next Execution
1. Download Kaggle CSV into `data/raw/Loan_default.csv`.
2. Run profiling script:
   - `python scripts/phase2_profile_dataset.py`
3. Use generated audit outputs to lock final data dictionary before cleaning.
