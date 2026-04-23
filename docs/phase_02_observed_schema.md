# Phase 2 Observed Schema Audit

- File: `/Users/riddhikhera/Desktop/loan_default/data/raw/Loan_default.csv`
- Rows: `255,347`
- Columns: `18`
- Duplicate rows: `0`
- Duplicate LoanID: `0`
- Default rate (%): `11.613`

## Schema Validation
- Missing expected columns: `[]`
- Unexpected columns: `[]`

## Column Dtypes
- `LoanID`: dtype=object, missing=0 (0.0%), unique=255347
- `Age`: dtype=int64, missing=0 (0.0%), unique=52
- `Income`: dtype=int64, missing=0 (0.0%), unique=114620
- `LoanAmount`: dtype=int64, missing=0 (0.0%), unique=158729
- `CreditScore`: dtype=int64, missing=0 (0.0%), unique=550
- `MonthsEmployed`: dtype=int64, missing=0 (0.0%), unique=120
- `NumCreditLines`: dtype=int64, missing=0 (0.0%), unique=4
- `InterestRate`: dtype=float64, missing=0 (0.0%), unique=2301
- `LoanTerm`: dtype=int64, missing=0 (0.0%), unique=5
- `DTIRatio`: dtype=float64, missing=0 (0.0%), unique=81
- `Education`: dtype=object, missing=0 (0.0%), unique=4
- `EmploymentType`: dtype=object, missing=0 (0.0%), unique=4
- `MaritalStatus`: dtype=object, missing=0 (0.0%), unique=3
- `HasMortgage`: dtype=object, missing=0 (0.0%), unique=2
- `HasDependents`: dtype=object, missing=0 (0.0%), unique=2
- `LoanPurpose`: dtype=object, missing=0 (0.0%), unique=5
- `HasCoSigner`: dtype=object, missing=0 (0.0%), unique=2
- `Default`: dtype=int64, missing=0 (0.0%), unique=2