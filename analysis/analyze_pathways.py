"""
CareFlow - Patient Pathway Analysis

Analyzes patient-level journey durations and
compares the different synthetic care pathways.
"""

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/pathway_analysis.csv"


# --------------------------------------------------
# Load event log
# --------------------------------------------------

def load_event_log():
    """
    Load the synthetic EHR event log.
    """

    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"]
    )

    return df


# --------------------------------------------------
# Identify pathway
# --------------------------------------------------

def identify_pathway(activities):
    """
    Identify the synthetic pathway based on
    the sequence of patient activities.
    """

    activity_sequence = " -> ".join(activities)

    if "X-Ray -> Triage" in activity_sequence:
        return "XRAY_LOOPBACK"

    if "X-Ray" in activity_sequence:
        return "XRAY"

    return "NORMAL"


# --------------------------------------------------
# Create patient-level analysis
# --------------------------------------------------

def create_patient_analysis(df):
    """
    Calculate journey-level metrics for each case.
    """

    patient_records = []

    for case_id, case_data in df.groupby("Case_ID"):

        case_data = case_data.sort_values(
            "Timestamp"
        )

        activities = case_data[
            "Activity_Name"
        ].tolist()

        start_time = case_data[
            "Timestamp"
        ].min()

        end_time = case_data[
            "Timestamp"
        ].max()

        total_duration = (
            end_time - start_time
        ).total_seconds() / 60

        pathway = identify_pathway(
            activities
        )

        loopback = (
            "X-Ray" in activities
            and "X-Ray -> Triage"
            in " -> ".join(activities)
        )

        patient_records.append(
            {
                "Case_ID": case_id,
                "Patient_ID": case_data[
                    "Patient_ID"
                ].iloc[0],
                "Pathway": pathway,
                "Activity_Count": len(activities),
                "Total_Duration_Minutes": round(
                    total_duration,
                    2,
                ),
                "Loopback": loopback,
                "Emergency_Level": case_data[
                    "Emergency_Level"
                ].iloc[0],
                "Age_Group": case_data[
                    "Age_Group"
                ].iloc[0],
                "Gender": case_data[
                    "Gender"
                ].iloc[0],
            }
        )

    return pd.DataFrame(patient_records)


# --------------------------------------------------
# Pathway summary
# --------------------------------------------------

def create_pathway_summary(patient_analysis):
    """
    Calculate summary statistics for each pathway.
    """

    summary = (
        patient_analysis
        .groupby("Pathway")
        .agg(
            Patient_Count=("Case_ID", "count"),
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
        )
        .reset_index()
    )

    summary[
        "Average_Duration_Minutes"
    ] = summary[
        "Average_Duration_Minutes"
    ].round(2)

    summary[
        "Minimum_Duration_Minutes"
    ] = summary[
        "Minimum_Duration_Minutes"
    ].round(2)

    summary[
        "Maximum_Duration_Minutes"
    ] = summary[
        "Maximum_Duration_Minutes"
    ].round(2)

    summary[
        "Average_Activity_Count"
    ] = summary[
        "Average_Activity_Count"
    ].round(2)

    return summary


# --------------------------------------------------
# Main execution
# --------------------------------------------------

if __name__ == "__main__":

    print("CareFlow - Patient Pathway Analysis")
    print("-" * 45)

    df = load_event_log()

    print("Events loaded:", len(df))
    print("Cases loaded:", df["Case_ID"].nunique())

    patient_analysis = create_patient_analysis(
        df
    )

    print("\nPatient-level analysis")
    print("----------------------")

    print(
        "Patients analyzed:",
        len(patient_analysis),
    )

    print(
        "Loop-back cases:",
        patient_analysis["Loopback"].sum(),
    )

    print("\nPathway distribution:")

    print(
        patient_analysis[
            "Pathway"
        ].value_counts()
    )

    summary = create_pathway_summary(
        patient_analysis
    )

    print("\nPathway duration summary")
    print("------------------------")

    print(
        summary.to_string(
            index=False
        )
    )

    patient_analysis.to_csv(
    OUTPUT_PATH,
    index=False,
)

    summary_output_path = (
    "analysis/pathway_summary.csv"
)

    summary.to_csv(
    summary_output_path,
    index=False,
)

    print(
    "\nPatient-level analysis saved to:"
)

    print(OUTPUT_PATH)

    print(
    "\nPathway summary saved to:"
)

    print(summary_output_path)

    print(
        "\nDay 7 pathway analysis completed!"
    )