
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# CareFlow - Day 23
# Automated Data Quality Validation
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILES = {
    "operational_kpi_report": BASE_DIR / "operational_kpi_report.csv",
    "executive_dashboard_data": BASE_DIR / "executive_dashboard_data.csv",
}

OUTPUT_FILE = BASE_DIR / "data_quality_report.csv"

checks = []


def record_check(dataset, check_name, passed, details):
    checks.append({
        "Dataset": dataset,
        "Check_Name": check_name,
        "Status": "PASS" if passed else "FAIL",
        "Details": str(details),
    })


# ---------------------------------------------------------
# Expected schemas
# ---------------------------------------------------------

expected_columns = {
    "operational_kpi_report": [
        "KPI_Category",
        "KPI_Name",
        "KPI_Value",
        "Unit",
    ],
    "executive_dashboard_data": [
        "KPI_Category",
        "Dashboard_Section",
        "KPI_Name",
        "KPI_Value",
        "Display_Value",
        "Unit",
        "Interpretation",
        "Data_Source",
        "Evidence_Type",
        "Caution",
    ],
}


# ---------------------------------------------------------
# Load and validate each dataset
# ---------------------------------------------------------

datasets = {}

for dataset_name, file_path in INPUT_FILES.items():

    if not file_path.exists():
        record_check(
            dataset_name,
            "File Exists",
            False,
            f"File not found: {file_path.name}",
        )
        continue

    record_check(
        dataset_name,
        "File Exists",
        True,
        f"Found {file_path.name}",
    )

    try:
        df = pd.read_csv(file_path)
        datasets[dataset_name] = df
    except Exception as exc:
        record_check(
            dataset_name,
            "CSV Readable",
            False,
            str(exc),
        )
        continue

    record_check(
        dataset_name,
        "CSV Readable",
        True,
        f"Loaded {len(df)} rows",
    )

    missing_columns = [
        col for col in expected_columns[dataset_name]
        if col not in df.columns
    ]

    record_check(
        dataset_name,
        "Required Columns",
        len(missing_columns) == 0,
        (
            "All required columns present"
            if not missing_columns
            else f"Missing columns: {missing_columns}"
        ),
    )

    if missing_columns:
        continue

    record_check(
        dataset_name,
        "No Missing Values",
        not df[expected_columns[dataset_name]].isnull().any().any(),
        f"Missing cells: {int(df[expected_columns[dataset_name]].isnull().sum().sum())}",
    )

    record_check(
        dataset_name,
        "Unique KPI Names",
        not df["KPI_Name"].duplicated().any(),
        f"Duplicate names: {int(df['KPI_Name'].duplicated().sum())}",
    )

    numeric_values = pd.to_numeric(
        df["KPI_Value"], errors="coerce"
    )

    record_check(
        dataset_name,
        "Numeric KPI Values",
        numeric_values.notna().all(),
        f"Invalid numeric values: {int(numeric_values.isna().sum())}",
    )

    record_check(
        dataset_name,
        "Non-Negative KPI Values",
        numeric_values.notna().all() and (numeric_values >= 0).all(),
        "All KPI values are non-negative"
        if numeric_values.notna().all() and (numeric_values >= 0).all()
        else "Invalid or negative KPI values found",
    )

    record_check(
        dataset_name,
        "Expected KPI Count",
        len(df) == 13,
        f"Observed {len(df)} rows; expected 13",
    )


# ---------------------------------------------------------
# Validate important KPI values
# ---------------------------------------------------------

if "operational_kpi_report" in datasets:
    kpi_df = datasets["operational_kpi_report"]

    if {"KPI_Name", "KPI_Value"}.issubset(kpi_df.columns):
        values = kpi_df.set_index("KPI_Name")["KPI_Value"]

        expected_values = {
            "Total Patients": 100,
            "Conforming Patients": 84,
            "Non-Conforming Patients": 16,
            "Loopback Patients": 16,
            "Loopback Rate": 16.0,
            "Simulated Reduction": 17.23,
        }

        for kpi_name, expected_value in expected_values.items():
            if kpi_name not in values.index:
                record_check(
                    "operational_kpi_report",
                    f"Expected KPI: {kpi_name}",
                    False,
                    "KPI not found",
                )
                continue

            observed = pd.to_numeric(
                pd.Series([values[kpi_name]]),
                errors="coerce"
            ).iloc[0]

            passed = (
                pd.notna(observed)
                and abs(observed - expected_value) < 0.011
            )

            record_check(
                "operational_kpi_report",
                f"Expected KPI: {kpi_name}",
                passed,
                f"Observed {observed}; expected {expected_value}",
            )


# ---------------------------------------------------------
# Cross-dataset consistency
# ---------------------------------------------------------

if (
    "operational_kpi_report" in datasets
    and "executive_dashboard_data" in datasets
):
    base_df = datasets["operational_kpi_report"]
    dashboard_df = datasets["executive_dashboard_data"]

    base_values = base_df.set_index("KPI_Name")["KPI_Value"]
    dashboard_values = dashboard_df.set_index("KPI_Name")["KPI_Value"]

    same_names = set(base_values.index) == set(dashboard_values.index)

    record_check(
        "Cross-dataset",
        "Matching KPI Names",
        same_names,
        "Both datasets contain the same KPI names"
        if same_names
        else "KPI names differ between datasets",
    )

    if same_names:
        base_numeric = pd.to_numeric(base_values).sort_index()
        dashboard_numeric = pd.to_numeric(dashboard_values).sort_index()

        same_values = (
            base_numeric.round(2).equals(
                dashboard_numeric.round(2)
            )
        )

        record_check(
            "Cross-dataset",
            "Matching KPI Values",
            same_values,
            "All KPI values match"
            if same_values
            else "KPI values differ between datasets",
        )


# ---------------------------------------------------------
# Save report and display results
# ---------------------------------------------------------

report = pd.DataFrame(checks)
report.to_csv(OUTPUT_FILE, index=False)

total_checks = len(report)
passed_checks = int((report["Status"] == "PASS").sum())
failed_checks = int((report["Status"] == "FAIL").sum())

print("=" * 65)
print("CAREFLOW - DAY 24")
print("AUTOMATED DATA QUALITY REPORT")
print("=" * 65)

print(f"Total checks: {total_checks}")
print(f"Passed: {passed_checks}")
print(f"Failed: {failed_checks}")

print("\nCheck results:")
print(report.to_string(index=False))

print(f"\nReport saved to: {OUTPUT_FILE}")

if failed_checks:
    print("\nDATA QUALITY VALIDATION FAILED.")
else:
    print("\nALL DATA QUALITY CHECKS PASSED.")

print("=" * 65)
