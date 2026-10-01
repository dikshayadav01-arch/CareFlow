"""
CareFlow - Conformance Impact Analysis

Analyzes the pathway duration and activity impact
of conforming and non-conforming synthetic patients.
"""

import pandas as pd


INPUT_PATH = "analysis/conformance_analysis.csv"
EVENT_LOG_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/conformance_impact_analysis.csv"


def load_data():
    conformance = pd.read_csv(INPUT_PATH)

    event_log = pd.read_csv(EVENT_LOG_PATH)

    event_log["Timestamp"] = pd.to_datetime(
        event_log["Timestamp"]
    )

    return conformance, event_log


def calculate_patient_duration(event_log):
    patient_duration = (
        event_log.groupby("Case_ID")
        .agg(
            Start_Time=("Timestamp", "min"),
            End_Time=("Timestamp", "max"),
        )
        .reset_index()
    )

    patient_duration["Total_Duration_Minutes"] = (
        patient_duration["End_Time"]
        - patient_duration["Start_Time"]
    ).dt.total_seconds() / 60

    patient_duration["Total_Duration_Minutes"] = (
        patient_duration["Total_Duration_Minutes"]
        .round(2)
    )

    return patient_duration


def create_impact_analysis(conformance, event_log):

    patient_duration = calculate_patient_duration(
        event_log
    )

    result = conformance.merge(
        patient_duration[
            [
                "Case_ID",
                "Total_Duration_Minutes",
            ]
        ],
        on="Case_ID",
        how="left",
    )

    result["Extra_Activities"] = (
        result["Activity_Count"] - 6
    )

    return result


def create_summary(result):

    summary = (
        result.groupby("Conformance_Status")
        .agg(
            Patient_Count=("Patient_ID", "nunique"),
            Average_Duration_Minutes=(
                "Total_Duration_Minutes",
                "mean",
            ),
            Minimum_Duration_Minutes=(
                "Total_Duration_Minutes",
                "min",
            ),
            Maximum_Duration_Minutes=(
                "Total_Duration_Minutes",
                "max",
            ),
            Average_Activity_Count=(
                "Activity_Count",
                "mean",
            ),
            Average_Extra_Activities=(
                "Extra_Activities",
                "mean",
            ),
        )
        .reset_index()
    )

    numeric_columns = [
        "Average_Duration_Minutes",
        "Minimum_Duration_Minutes",
        "Maximum_Duration_Minutes",
        "Average_Activity_Count",
        "Average_Extra_Activities",
    ]

    summary[numeric_columns] = (
        summary[numeric_columns].round(2)
    )

    return summary


if __name__ == "__main__":

    print("CareFlow - Conformance Impact Analysis")
    print("-" * 50)

    conformance, event_log = load_data()

    print("Conformance records:", len(conformance))
    print("Event records:", len(event_log))

    result = create_impact_analysis(
        conformance,
        event_log,
    )

    summary = create_summary(result)

    print("\nConformance Impact Summary")
    print("-" * 50)
    print(summary.to_string(index=False))

    print("\nDetailed Impact")
    print("-" * 50)

    print(
        result[
            [
                "Case_ID",
                "Conformance_Status",
                "Activity_Count",
                "Extra_Activities",
                "Total_Duration_Minutes",
            ]
        ]
        .head(10)
        .to_string(index=False)
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print("\nImpact analysis saved to:")
    print(OUTPUT_PATH)

    print("\nDay 15 conformance impact analysis completed!")