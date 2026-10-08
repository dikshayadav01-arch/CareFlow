import pandas as pd
from pathlib import Path


# ---------------------------------------------------------
# CareFlow - Day 21
# Create Unified Operational KPI Report
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent


# ---------------------------------------------------------
# Load existing analysis outputs
# ---------------------------------------------------------

conformance_summary_path = BASE_DIR / "conformance_summary.csv"
conformance_impact_path = BASE_DIR / "conformance_impact_analysis.csv"
bottleneck_impact_path = BASE_DIR / "bottleneck_impact_analysis.csv"
improvement_path = BASE_DIR / "bottleneck_improvement_simulation.csv"


conformance_summary = pd.read_csv(conformance_summary_path)
conformance_impact = pd.read_csv(conformance_impact_path)
bottleneck_impact = pd.read_csv(bottleneck_impact_path)
improvement = pd.read_csv(improvement_path)


# ---------------------------------------------------------
# Extract KPI values
# ---------------------------------------------------------

total_patients = len(conformance_impact)

conforming_patients = (
    conformance_impact["Conformance_Status"]
    .eq("CONFORMING")
    .sum()
)

non_conforming_patients = (
    conformance_impact["Conformance_Status"]
    .eq("NON_CONFORMING")
    .sum()
)

conforming_avg_duration = (
    conformance_impact[
        conformance_impact["Conformance_Status"] == "CONFORMING"
    ]["Total_Duration_Minutes"]
    .mean()
)

non_conforming_avg_duration = (
    conformance_impact[
        conformance_impact["Conformance_Status"] == "NON_CONFORMING"
    ]["Total_Duration_Minutes"]
    .mean()
)

loopback_patients = (
    conformance_impact["Actual_Pathway"]
    .str.contains("X-Ray -> Triage", regex=False)
    .sum()
)


loopback_rate = (
    loopback_patients / total_patients * 100
)

additional_time_per_patient = (
    non_conforming_avg_duration - conforming_avg_duration
)


# ---------------------------------------------------------
# Bottleneck impact values
# ---------------------------------------------------------

affected_percentage = bottleneck_impact.loc[
    0, "Affected_Patient_Percentage"
]

estimated_additional_minutes = bottleneck_impact.loc[
    0, "Estimated_Total_Additional_Minutes"
]


# ---------------------------------------------------------
# Bottleneck improvement simulation values
# ---------------------------------------------------------

simulated_reduction_per_patient = improvement.loc[
    0, "Simulated_Duration_Reduction_Per_Patient"
]

simulated_reduction_percentage = improvement.loc[
    0, "Simulated_Reduction_Percentage"
]

total_simulated_time_reduction = improvement.loc[
    0, "Total_Simulated_Time_Reduction_Minutes"
]


# ---------------------------------------------------------
# Create unified KPI dataset
# ---------------------------------------------------------

kpis = [
    {
        "KPI_Category": "Patient Volume",
        "KPI_Name": "Total Patients",
        "KPI_Value": total_patients,
        "Unit": "patients",
    },
    {
        "KPI_Category": "Conformance",
        "KPI_Name": "Conforming Patients",
        "KPI_Value": conforming_patients,
        "Unit": "patients",
    },
    {
        "KPI_Category": "Conformance",
        "KPI_Name": "Non-Conforming Patients",
        "KPI_Value": non_conforming_patients,
        "Unit": "patients",
    },
    {
        "KPI_Category": "Pathway Deviation",
        "KPI_Name": "Loopback Patients",
        "KPI_Value": loopback_patients,
        "Unit": "patients",
    },
    {
        "KPI_Category": "Pathway Deviation",
        "KPI_Name": "Loopback Rate",
        "KPI_Value": loopback_rate,
        "Unit": "percent",
    },
    {
        "KPI_Category": "Pathway Performance",
        "KPI_Name": "Conforming Average Duration",
        "KPI_Value": conforming_avg_duration,
        "Unit": "minutes",
    },
    {
        "KPI_Category": "Pathway Performance",
        "KPI_Name": "Non-Conforming Average Duration",
        "KPI_Value": non_conforming_avg_duration,
        "Unit": "minutes",
    },
    {
        "KPI_Category": "Bottleneck Impact",
        "KPI_Name": "Affected Patient Percentage",
        "KPI_Value": affected_percentage,
        "Unit": "percent",
    },
    {
        "KPI_Category": "Bottleneck Impact",
        "KPI_Name": "Additional Time Per Affected Patient",
        "KPI_Value": additional_time_per_patient,
        "Unit": "minutes",
    },
    {
        "KPI_Category": "Bottleneck Impact",
        "KPI_Name": "Estimated Additional Time",
        "KPI_Value": estimated_additional_minutes,
        "Unit": "minutes",
    },
    {
        "KPI_Category": "Improvement Simulation",
        "KPI_Name": "Simulated Duration Reduction Per Patient",
        "KPI_Value": simulated_reduction_per_patient,
        "Unit": "minutes",
    },
    {
        "KPI_Category": "Improvement Simulation",
        "KPI_Name": "Simulated Reduction",
        "KPI_Value": simulated_reduction_percentage,
        "Unit": "percent",
    },
    {
        "KPI_Category": "Improvement Simulation",
        "KPI_Name": "Total Simulated Time Reduction",
        "KPI_Value": total_simulated_time_reduction,
        "Unit": "minutes",
    },
]


kpi_df = pd.DataFrame(kpis)


# ---------------------------------------------------------
# Round numerical values
# ---------------------------------------------------------

kpi_df["KPI_Value"] = kpi_df["KPI_Value"].round(2)


# ---------------------------------------------------------
# Save report
# ---------------------------------------------------------

output_path = BASE_DIR / "operational_kpi_report.csv"

kpi_df.to_csv(output_path, index=False)


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

print("=" * 60)
print("CAREFLOW - DAY 22")
print("UNIFIED OPERATIONAL KPI REPORT")
print("=" * 60)

print(f"Total KPIs: {len(kpi_df)}")
print(f"Missing values: {kpi_df.isnull().sum().sum()}")
print()

print(kpi_df.to_string(index=False))

print()
print(f"Report saved to: {output_path}")
print("=" * 60)