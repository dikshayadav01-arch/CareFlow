import sys
from datetime import datetime
from pathlib import Path

import pandas as pd


# ---------------------------------------------------------
# CareFlow - Day 26
# Validation History Tracking
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

PIPELINE_REPORT = BASE_DIR / "validation_pipeline_report.csv"
HISTORY_FILE = BASE_DIR / "validation_history.csv"


def main():
    if not PIPELINE_REPORT.exists():
        print(f"ERROR: Pipeline report not found: {PIPELINE_REPORT}")
        sys.exit(1)

    report = pd.read_csv(PIPELINE_REPORT)

    required_columns = {
        "Pipeline_Name",
        "Total_Checks",
        "Passed_Checks",
        "Failed_Checks",
        "Unexpected_Statuses",
        "Pipeline_Status",
    }

    missing_columns = required_columns - set(report.columns)

    if missing_columns:
        print(f"ERROR: Missing report columns: {sorted(missing_columns)}")
        sys.exit(1)

    if len(report) != 1:
        print("ERROR: Expected exactly one pipeline summary row.")
        sys.exit(1)

    result = report.iloc[0]

    record = pd.DataFrame([{
        "Run_Timestamp": datetime.now().astimezone().isoformat(
            timespec="seconds"
        ),
        "Pipeline_Name": result["Pipeline_Name"],
        "Total_Checks": int(result["Total_Checks"]),
        "Passed_Checks": int(result["Passed_Checks"]),
        "Failed_Checks": int(result["Failed_Checks"]),
        "Unexpected_Statuses": int(result["Unexpected_Statuses"]),
        "Pipeline_Status": result["Pipeline_Status"],
    }])

    if HISTORY_FILE.exists():
        history = pd.read_csv(HISTORY_FILE)

        if list(history.columns) != list(record.columns):
            print("ERROR: Existing history file has an unexpected schema.")
            sys.exit(1)

        history = pd.concat([history, record], ignore_index=True)
    else:
        history = record

    history.to_csv(HISTORY_FILE, index=False)

    print("=" * 60)
    print("CAREFLOW - DAY 26")
    print("VALIDATION HISTORY TRACKING")
    print("=" * 60)
    print(f"Recorded pipeline status: {record.iloc[0]['Pipeline_Status']}")
    print(f"Total checks: {record.iloc[0]['Total_Checks']}")
    print(f"Passed checks: {record.iloc[0]['Passed_Checks']}")
    print(f"Failed checks: {record.iloc[0]['Failed_Checks']}")
    print(f"History records: {len(history)}")
    print(f"History file: {HISTORY_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()