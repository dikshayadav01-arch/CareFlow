"""
CareFlow - Emergency Level Analysis

Analyzes patient pathway duration across different
synthetic emergency levels.
"""

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_PATH = "data/raw/ehr_event_log.csv"

OUTPUT_PATH = (
    "analysis/emergency_level_analysis.csv"
)


# --------------------------------------------------
# Load event log
# --------------------------------------------------

def load_event_log():
    """
    Load and prepare the synthetic EHR event log.
    """

    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"]
    )

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df


# --------------------------------------------------
# Create patient-level duration data
# --------------------------------------------------

def create_patient_analysis(df):
    """
    Calculate total journey duration for each patient case.
    """

    patient_records = []

    for case_id, case_data in df.groupby(
        "Case_ID"
    ):

        case_data = case_data.sort_values(
            "Timestamp"
        )

        start_time = case_data[
            "Timestamp"
        ].min()

        end_time = case_data[
            "Timestamp"
        ].max()

        total_duration = (
            end_time - start_time
        ).total_seconds() / 60

        patient_records.append(
            {
                "Case_ID": case_id,
                "Patient_ID": case_data[
                    "Patient_ID"
                ].iloc[0],
                "Emergency_Level": case_data[
                    "Emergency_Level"
                ].iloc[0],
                "Total_Duration_Minutes": round(
                    total_duration,
                    2,
                ),
                "Activity_Count": len(
                    case_data
                ),
            }
        )

    return pd.DataFrame(
        patient_records
    )


# --------------------------------------------------
# Analyze emergency levels
# --------------------------------------------------

def analyze_emergency_levels(
    patient_analysis
):
    """
    Calculate duration statistics for each
    emergency level.
    """

    summary = (
        patient_analysis
        .groupby("Emergency_Level")
        .agg(
            Patient_Count=(
                "Case_ID",
                "count",
            ),
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

    total_patients = summary[
        "Patient_Count"
    ].sum()

    summary["Patient_Percentage"] = (
        summary["Patient_Count"]
        / total_patients
        * 100
    ).round(2)

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

    print(
        "CareFlow - Emergency Level Analysis"
    )

    print("-" * 50)

    df = load_event_log()

    print(
        "Events loaded:",
        len(df)
    )

    print(
        "Cases loaded:",
        df["Case_ID"].nunique()
    )

    patient_analysis = create_patient_analysis(
        df
    )

    print(
        "\nPatients analyzed:",
        len(patient_analysis)
    )

    summary = analyze_emergency_levels(
        patient_analysis
    )

    print(
        "\nEmergency level analysis"
    )

    print("-" * 50)

    print(
        summary.to_string(
            index=False
        )
    )

    summary.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nEmergency level analysis saved to:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "\nDay 9 emergency level analysis completed!"
    )