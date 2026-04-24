"""Phase 8 KPI framework calculator for SmartCredit."""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def safe_div(num: float, den: float) -> float:
    return float(num / den) if den else 0.0


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    clean_path = root / "data" / "processed" / "loan_clean.csv"
    raw_path = root / "data" / "raw" / "Loan_default.csv"
    score_path = root / "data" / "processed" / "phase_07_default_probability_scores.csv"

    if clean_path.exists():
        df = pd.read_csv(clean_path)
    elif raw_path.exists():
        df = pd.read_csv(raw_path)
    else:
        print("No input found. Provide data/raw/Loan_default.csv or run Phase 5 first.")
        return

    total = len(df)
    defaults = int(df["Default"].sum())
    non_defaults = int(total - defaults)

    if "IncomeToLoanRatio" not in df.columns and {"Income", "LoanAmount"}.issubset(df.columns):
        df["IncomeToLoanRatio"] = (df["Income"] / df["LoanAmount"]).replace([np.inf, -np.inf], np.nan).fillna(0)

    kpis = []
    kpis.append(("KPI01", "Total Loans", total, "count(LoanID)"))
    kpis.append(("KPI02", "Default Rate %", round(safe_div(defaults, total) * 100, 3), "sum(Default)/count(LoanID)*100"))
    kpis.append(("KPI03", "Non-Default Rate %", round(safe_div(non_defaults, total) * 100, 3), "(count(LoanID)-sum(Default))/count(LoanID)*100"))
    kpis.append(("KPI04", "Average Loan Size", round(float(df["LoanAmount"].mean()), 2), "avg(LoanAmount)"))
    kpis.append(("KPI05", "Average Income", round(float(df["Income"].mean()), 2), "avg(Income)"))
    kpis.append(("KPI06", "Income to Loan Ratio", round(float(df["IncomeToLoanRatio"].mean()), 4), "avg(Income/LoanAmount)"))
    kpis.append(("KPI07", "High DTI Ratio %", round(float((df["DTIRatio"] > 0.50).mean() * 100), 3), "count(DTIRatio>0.50)/count(LoanID)*100"))
    kpis.append(("KPI08", "Low Credit Score Ratio %", round(float((df["CreditScore"] < 580).mean() * 100), 3), "count(CreditScore<580)/count(LoanID)*100"))
    kpis.append(("KPI09", "Avg Interest Rate", round(float(df["InterestRate"].mean()), 4), "avg(InterestRate)"))
    kpis.append(("KPI10", "Average DTI", round(float(df["DTIRatio"].mean()), 4), "avg(DTIRatio)"))
    kpis.append(("KPI11", "Avg Credit Score", round(float(df["CreditScore"].mean()), 3), "avg(CreditScore)"))
    kpis.append(("KPI12", "Avg Months Employed", round(float(df["MonthsEmployed"].mean()), 3), "avg(MonthsEmployed)"))
    kpis.append(("KPI13", "Co-signer Penetration %", round(float((df["HasCoSigner"].astype(str).str.lower() == "yes").mean() * 100), 3), "count(HasCoSigner='Yes')/count(LoanID)*100"))
    kpis.append(("KPI14", "Mortgage Holder Share %", round(float((df["HasMortgage"].astype(str).str.lower() == "yes").mean() * 100), 3), "count(HasMortgage='Yes')/count(LoanID)*100"))
    kpis.append(("KPI15", "Dependents Share %", round(float((df["HasDependents"].astype(str).str.lower() == "yes").mean() * 100), 3), "count(HasDependents='Yes')/count(LoanID)*100"))

    purpose_risk = (
        df.groupby("LoanPurpose", as_index=False)["Default"].mean().assign(DefaultRatePct=lambda x: x["Default"] * 100)
    )
    top_purpose = purpose_risk.sort_values("DefaultRatePct", ascending=False).iloc[0]
    kpis.append(("KPI16", "Highest Risk Loan Purpose Default %", round(float(top_purpose["DefaultRatePct"]), 3), "max(default_rate by LoanPurpose)"))

    emp_risk = (
        df.groupby("EmploymentType", as_index=False)["Default"].mean().assign(DefaultRatePct=lambda x: x["Default"] * 100)
    )
    top_emp = emp_risk.sort_values("DefaultRatePct", ascending=False).iloc[0]
    kpis.append(("KPI17", "Highest Risk Employment Type Default %", round(float(top_emp["DefaultRatePct"]), 3), "max(default_rate by EmploymentType)"))

    default_cosigner_share = safe_div(
        len(df[(df["Default"] == 1) & (df["HasCoSigner"].astype(str).str.lower() == "yes")]),
        defaults,
    )
    kpis.append(("KPI18", "Recovery Opportunity %", round(default_cosigner_share * 100, 3), "default_loans_with_cosigner/default_loans*100"))

    high_risk_ratio = 0.0
    top30_default_capture = 0.0
    if score_path.exists():
        scored = pd.read_csv(score_path)
        high_risk_ratio = float(scored["risk_band"].isin(["High", "Very High"]).mean() * 100)
        scored = scored.sort_values("default_probability", ascending=False).reset_index(drop=True)
        cutoff = int(np.ceil(0.30 * len(scored)))
        top30 = scored.iloc[:cutoff]
        top30_default_capture = safe_div(top30["actual_default"].sum(), scored["actual_default"].sum()) * 100
    kpis.append(("KPI19", "High Risk Ratio %", round(high_risk_ratio, 3), "count(risk_band in High/Very High)/count(scored_loans)*100"))
    kpis.append(("KPI20", "Top-30% Risk Default Capture %", round(top30_default_capture, 3), "defaults_in_top30pct_risk/total_defaults*100"))

    kpi_df = pd.DataFrame(kpis, columns=["kpi_id", "kpi_name", "kpi_value", "formula"])

    # Weighted portfolio health index, 0-100 (higher is healthier).
    default_rate = safe_div(defaults, total)
    high_dti = float((df["DTIRatio"] > 0.50).mean())
    low_score = float((df["CreditScore"] < 580).mean())
    health_score = max(0.0, 100 - (default_rate * 45 + high_dti * 30 + low_score * 25) * 100)
    health_df = pd.DataFrame([
        {
            "metric": "Portfolio Health Score",
            "value": round(health_score, 3),
            "formula": "100 - (DefaultRate*45 + HighDTIRatio*30 + LowCreditRatio*25)",
        }
    ])

    out_values = root / "data" / "processed" / "phase_08_kpi_values.csv"
    out_health = root / "data" / "processed" / "phase_08_portfolio_health_score.csv"
    out_md = root / "reports" / "phase_08_kpi_scorecard.md"

    out_values.parent.mkdir(parents=True, exist_ok=True)
    kpi_df.to_csv(out_values, index=False)
    health_df.to_csv(out_health, index=False)

    lines = [
        "# Phase 8 KPI Scorecard",
        "",
        f"- Total Loans: {total:,}",
        f"- Default Rate (%): {round(default_rate * 100, 3)}",
        f"- Portfolio Health Score: {round(health_score, 3)}",
        f"- Top Risk Loan Purpose: {top_purpose['LoanPurpose']} ({round(float(top_purpose['DefaultRatePct']), 3)}%)",
        f"- Top Risk Employment Type: {top_emp['EmploymentType']} ({round(float(top_emp['DefaultRatePct']), 3)}%)",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")

    print("Phase 8 KPI framework completed.")
    print(f"Saved: {out_values}")
    print(f"Saved: {out_health}")
    print(f"Saved: {out_md}")


if __name__ == "__main__":
    main()
