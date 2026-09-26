"""
CareFlow - Doctor-Level Analysis

Analyzes patient pathway duration across doctors
using the synthetic EHR event log.
"""

import pandas as pd

INPUT_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/doctor_level_analysis.csv"


def load_event_log():
    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"]
    )

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df


def create_patient_analysis(df):
    patient_records = []

    for case_id, case_data in df.groupby("Case_ID"):

        case_data = case_data.sort_values("Timestamp")

        start_time = case_data["Timestamp"].min()
        end_time = case_data["Timestamp"].max()

        total_duration = (
            end_time - start_time
        ).total_seconds() / 60

        patient_records.append({
            "Case_ID": case_id,
            "Patient_ID": case_data["Patient_ID"].iloc[0],
            "Doctor": case_data["Doctor"].iloc[0],
            "Emergency_Level": case_data["Emergency_Level"].iloc[0],
            "Total_Duration_Minutes": round(
                total_duration, 2
            ),
            "Activity_Count": len(case_data),
        })

    return pd.DataFrame(patient_records)


def analyze_doctors(patient_analysis):

    summary = (
        patient_analysis
        .groupby("Doctor")
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

    total_patients = summary[
        "Patient_Count"
    ].sum()

    summary["Patient_Percentage"] = (
        summary["Patient_Count"]
        / total_patients
        * 100
    ).round(2)

    summary["Average_Duration_Minutes"] = (
        summary["Average_Duration_Minutes"]
        .round(2)
    )

    summary["Minimum_Duration_Minutes"] = (
        summary["Minimum_Duration_Minutes"]
        .round(2)
    )

    summary["Maximum_Duration_Minutes"] = (
        summary["Maximum_Duration_Minutes"]
        .round(2)
    )

    summary["Average_Activity_Count"] = (
        summary["Average_Activity_Count"]
        .round(2)
    )

    return summary


if __name__ == "__main__":

    print("CareFlow - Doctor-Level Analysis")
    print("-" * 50)

    df = load_event_log()

    print("Events loaded:", len(df))
    print("Cases loaded:", df["Case_ID"].nunique())

    patient_analysis = create_patient_analysis(df)

    print(
        "\nPatients analyzed:",
        len(patient_analysis)
    )

    summary = analyze_doctors(
        patient_analysis
    )

    print("\nDoctor-level analysis")
    print("-" * 50)

    print(
        summary.to_string(index=False)
    )

    summary.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nDoctor-level analysis saved to:"
    )

    print(OUTPUT_PATH)

    print(
        "\nDay 10 doctor-level analysis completed!"
    )