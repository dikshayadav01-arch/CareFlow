import subprocess
import sys
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# CareFlow - Day 25
# Reusable Validation Pipeline
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

VALIDATION_SCRIPT = BASE_DIR / "validate_operational_data.py"
QUALITY_REPORT = BASE_DIR / "data_quality_report.csv"
PIPELINE_REPORT = BASE_DIR / "validation_pipeline_report.csv"


def main():
    print("=" * 65)
    print("CAREFLOW - DAY 25")
    print("REUSABLE VALIDATION PIPELINE")
    print("=" * 65)

    if not VALIDATION_SCRIPT.exists():
        print(f"ERROR: Validation script not found: {VALIDATION_SCRIPT}")
        sys.exit(1)

    print("\nStep 1: Running data quality validation...")

    result = subprocess.run(
        [sys.executable, str(VALIDATION_SCRIPT)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR.parent),
    )

    print(result.stdout)

    if result.returncode != 0:
        print("ERROR: Validation script execution failed.")
        print(result.stderr)
        sys.exit(result.returncode)

    print("\nStep 2: Reading validation results...")

    if not QUALITY_REPORT.exists():
        print("ERROR: Data quality report was not generated.")
        sys.exit(1)

    report = pd.read_csv(QUALITY_REPORT)

    required_columns = {"Dataset", "Check_Name", "Status", "Details"}

    if not required_columns.issubset(report.columns):
        print("ERROR: Validation report has an unexpected schema.")
        sys.exit(1)

    total_checks = len(report)
    passed_checks = int((report["Status"] == "PASS").sum())
    failed_checks = int((report["Status"] == "FAIL").sum())

    unexpected_statuses = int(
        (~report["Status"].isin(["PASS", "FAIL"])).sum()
    )

    pipeline_status = (
        "PASS"
        if total_checks > 0
        and passed_checks == total_checks
        and failed_checks == 0
        and unexpected_statuses == 0
        else "FAIL"
    )

    summary = pd.DataFrame([{
        "Pipeline_Name": "CareFlow Data Quality Pipeline",
        "Total_Checks": total_checks,
        "Passed_Checks": passed_checks,
        "Failed_Checks": failed_checks,
        "Unexpected_Statuses": unexpected_statuses,
        "Pipeline_Status": pipeline_status,
    }])

    summary.to_csv(PIPELINE_REPORT, index=False)

    print("\nStep 3: Pipeline summary")
    print("-" * 65)
    print(summary.to_string(index=False))
    print(f"\nPipeline report saved to: {PIPELINE_REPORT}")

    if pipeline_status != "PASS":
        print("\nPIPELINE FAILED. Review the data quality report.")
        sys.exit(1)

    print("\nPIPELINE COMPLETED SUCCESSFULLY.")
    print("=" * 65)


if __name__ == "__main__":
    main()