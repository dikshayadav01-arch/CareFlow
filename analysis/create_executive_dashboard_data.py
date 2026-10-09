
import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# CareFlow - Day 22
# Prepare Executive Dashboard Dataset
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = BASE_DIR / "operational_kpi_report.csv"
OUTPUT_FILE = BASE_DIR / "executive_dashboard_data.csv"


# ---------------------------------------------------------
# Load and validate the Day 21 KPI report
# ---------------------------------------------------------

if not INPUT_FILE.exists():
    raise FileNotFoundError(
        f"Required KPI report not found: {INPUT_FILE}"
    )

df = pd.read_csv(INPUT_FILE)

required_columns = [
    "KPI_Category",
    "KPI_Name",
    "KPI_Value",
    "Unit",
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Missing required columns: {missing_columns}"
    )

if df["KPI_Name"].duplicated().any():
    raise ValueError("Duplicate KPI names found.")

if df[required_columns].isnull().any().any():
    raise ValueError("Missing values found in KPI report.")


# ---------------------------------------------------------
# Add dashboard-friendly labels and interpretations
# ---------------------------------------------------------

dashboard_labels = {
    "Total Patients": (
        "Patient Volume",
        "Total number of simulated patient cases."
    ),
    "Conforming Patients": (
        "Process Conformance",
        "Patients following one of the defined ideal pathways."
    ),
    "Non-Conforming Patients": (
        "Process Conformance",
        "Patients whose pathways differ from the defined ideal paths."
    ),
    "Loopback Patients": (
        "Pathway Deviations",
        "Patients whose simulated pathways return from X-Ray to Triage."
    ),
    "Loopback Rate": (
        "Pathway Deviations",
        "Percentage of simulated patients with an X-Ray-to-Triage loopback."
    ),
    "Conforming Average Duration": (
        "Pathway Performance",
        "Average pathway duration among conforming simulated patients."
    ),
    "Non-Conforming Average Duration": (
        "Pathway Performance",
        "Average pathway duration among non-conforming simulated patients."
    ),
    "Affected Patient Percentage": (
        "Bottleneck Impact",
        "Share of simulated patients classified as affected by the bottleneck."
    ),
    "Additional Time Per Affected Patient": (
        "Bottleneck Impact",
        "Difference between non-conforming and conforming average durations."
    ),
    "Estimated Additional Time": (
        "Bottleneck Impact",
        "Estimated aggregate duration difference in the synthetic dataset."
    ),
    "Simulated Duration Reduction Per Patient": (
        "Improvement Simulation",
        "Modeled duration reduction per affected patient under the simulation."
    ),
    "Simulated Reduction": (
        "Improvement Simulation",
        "Modeled percentage reduction under the improvement scenario."
    ),
    "Total Simulated Time Reduction": (
        "Improvement Simulation",
        "Modeled aggregate time reduction under the improvement scenario."
    ),
}


df["Dashboard_Section"] = df["KPI_Name"].map(
    lambda name: dashboard_labels.get(
        name, ("Other", "No interpretation provided.")
    )[0]
)

df["Interpretation"] = df["KPI_Name"].map(
    lambda name: dashboard_labels.get(
        name, ("Other", "No interpretation provided.")
    )[1]
)


# ---------------------------------------------------------
# Add presentation-friendly value strings
# ---------------------------------------------------------

def format_value(row):
    value = row["KPI_Value"]
    unit = row["Unit"]

    if unit == "percent":
        return f"{value:.2f}%"

    if unit == "minutes":
        return f"{value:.2f} min"

    if unit == "patients":
        return f"{value:.0f}"

    return str(value)


df["Display_Value"] = df.apply(format_value, axis=1)


# ---------------------------------------------------------
# Add source and interpretation safeguards
# ---------------------------------------------------------

df["Data_Source"] = "Synthetic CareFlow analysis"

df["Evidence_Type"] = df["KPI_Category"].apply(
    lambda category: (
        "Simulated scenario"
        if category == "Improvement Simulation"
        else "Synthetic-data analysis"
    )
)

df["Caution"] = (
    "Synthetic demonstration only; not a real hospital outcome."
)


# ---------------------------------------------------------
# Set useful column order and save
# ---------------------------------------------------------

df = df[
    [
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
    ]
]

df.to_csv(OUTPUT_FILE, index=False)


# ---------------------------------------------------------
# Validate and display results
# ---------------------------------------------------------

saved_df = pd.read_csv(OUTPUT_FILE)

print("=" * 65)
print("CAREFLOW - DAY 23")
print("EXECUTIVE DASHBOARD DATASET")
print("=" * 65)

print(f"Rows: {len(saved_df)}")
print(f"Columns: {len(saved_df.columns)}")
print(f"Missing values: {saved_df.isnull().sum().sum()}")
print(
    "Duplicate KPI names:",
    saved_df["KPI_Name"].duplicated().sum()
)
print("\nDashboard sections:")
print(saved_df["Dashboard_Section"].value_counts().to_string())

print("\nDataset preview:")
print(
    saved_df[
        ["Dashboard_Section", "KPI_Name", "Display_Value"]
    ].to_string(index=False)
)

print(f"\nSaved to: {OUTPUT_FILE}")
print("=" * 65)