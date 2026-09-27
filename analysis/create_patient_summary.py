"""
CareFlow - Dashboard Patient Summary

Creates a patient-level summary dataset for
future dashboard and Power BI analysis.
"""

import pandas as pd

INPUT_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/dashboard_patient_summary.csv"


def load_event_log():
    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"]
    )

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df


def determine_pathway(activities):
    activities = list(activities)

    if activities == [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "Investigation",
        "Treatment",
        "Discharge",
    ]:
        return "NORMAL"

    if activities == [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Treatment",
        "Discharge",
    ]:
        return "XRAY"

    if activities == [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Triage",
        "Doctor Consultation",
        "Treatment",
        "Discharge",
    ]:
        return "XRAY_LOOPBACK"

    return "OTHER"


def create_patient_summary(df):

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

        patient_records.append({
            "Case_ID": case_id,
            "Patient_ID": case_data[
                "Patient_ID"
            ].iloc[0],
            "Pathway": determine_pathway(
                activities
            ),
            "Emergency_Level": case_data[
                "Emergency_Level"
            ].iloc[0],
            "Doctor": case_data[
                "Doctor"
            ].iloc[0],
            "Age_Group": case_data[
                "Age_Group"
            ].iloc[0],
            "Gender": case_data[
                "Gender"
            ].iloc[0],
            "Activity_Count": len(
                activities
            ),
            "Total_Duration_Minutes": round(
                total_duration,
                2
            ),
            "Start_Time": start_time,
            "End_Time": end_time,
            "Loopback_Flag": (
                "X-Ray" in activities
                and activities.count("Triage") > 1
            ),
        })

    return pd.DataFrame(patient_records)


if __name__ == "__main__":

    print(
        "CareFlow - Dashboard Patient Summary"
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

    summary = create_patient_summary(df)

    print(
        "\nPatients summarized:",
        len(summary)
    )

    print(
        "\nPathway distribution"
    )
    print("-" * 50)

    print(
        summary["Pathway"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print(
        "\nLoop-back patients:",
        summary["Loopback_Flag"].sum()
    )

    print(
        "\nDashboard patient summary"
    )
    print("-" * 50)

    print(
        summary.to_string(index=False)
    )

    summary.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nDashboard patient summary saved to:"
    )

    print(OUTPUT_PATH)

    print(
        "\nDay 11 dashboard patient summary completed!"
    )