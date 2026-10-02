"""
CareFlow - Patient Pathway Deviation Analysis

Identifies where actual patient pathways differ
from the ideal synthetic patient pathways.
"""

import pandas as pd

INPUT_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/pathway_deviation_analysis.csv"
SUMMARY_PATH = "analysis/pathway_deviation_summary.csv"

IDEAL_PATHWAYS = {
    "NORMAL": [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "Investigation",
        "Treatment",
        "Discharge",
    ],
    "XRAY": [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Treatment",
        "Discharge",
    ],
}


def load_event_log():
    df = pd.read_csv(INPUT_PATH)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    return df.sort_values(
        ["Case_ID", "Timestamp"]
    ).reset_index(drop=True)


def identify_pathway(activities):
    if activities == IDEAL_PATHWAYS["NORMAL"]:
        return "NORMAL"

    if activities == IDEAL_PATHWAYS["XRAY"]:
        return "XRAY"

    if (
        activities.count("Triage") > 1
        and activities.count("Doctor Consultation") > 1
        and "X-Ray" in activities
    ):
        return "XRAY_LOOPBACK"

    return "UNKNOWN"


def find_deviation(activities, ideal):
    for index, activity in enumerate(activities):
        if index >= len(ideal):
            return (
                index + 1,
                activity,
                "EXTRA_ACTIVITY",
            )

        if activity != ideal[index]:
            return (
                index + 1,
                activity,
                "ACTIVITY_MISMATCH",
            )

    if len(activities) < len(ideal):
        return (
            len(activities) + 1,
            "MISSING_ACTIVITY",
            "MISSING_ACTIVITY",
        )

    return None, None, "NO_DEVIATION"


def analyze_deviations(df):
    records = []

    for case_id, case_data in df.groupby("Case_ID"):
        activities = case_data["Activity_Name"].tolist()
        pathway = identify_pathway(activities)

        if pathway in IDEAL_PATHWAYS:
            ideal = IDEAL_PATHWAYS[pathway]
            deviation = find_deviation(activities, ideal)
        elif pathway == "XRAY_LOOPBACK":
            ideal = IDEAL_PATHWAYS["XRAY"]
            deviation = (5, "Triage", "EXTRA_ACTIVITY")
        else:
            ideal = []
            deviation = (None, None, "UNKNOWN_PATHWAY")

        position, activity, deviation_type = deviation

        records.append({
            "Case_ID": case_id,
            "Patient_ID": case_data["Patient_ID"].iloc[0],
            "Actual_Pathway": pathway,
            "Activity_Count": len(activities),
            "Deviation_Position": position,
            "Deviation_Activity": activity,
            "Deviation_Type": deviation_type,
            "Deviation_Flag": int(
                deviation_type != "NO_DEVIATION"
            ),
        })

    return pd.DataFrame(records)


def create_summary(result):
    summary = (
        result.groupby(
            ["Actual_Pathway", "Deviation_Type"]
        )
        .agg(
            Patient_Count=("Patient_ID", "nunique"),
            Average_Activity_Count=("Activity_Count", "mean"),
        )
        .reset_index()
    )

    summary["Patient_Percentage"] = (
        summary["Patient_Count"]
        / summary["Patient_Count"].sum()
        * 100
    ).round(2)

    summary["Average_Activity_Count"] = (
        summary["Average_Activity_Count"].round(2)
    )

    return summary


if __name__ == "__main__":
    print("CareFlow - Patient Pathway Deviation Analysis")
    print("-" * 55)

    df = load_event_log()
    print("Events loaded:", len(df))
    print("Cases loaded:", df["Case_ID"].nunique())

    result = analyze_deviations(df)
    summary = create_summary(result)

    print("\nDeviation Type Counts")
    print("-" * 55)
    print(result["Deviation_Type"].value_counts().to_string())

    print("\nDeviation Summary")
    print("-" * 55)
    print(summary.to_string(index=False))

    print("\nSample Deviation Records")
    print("-" * 55)
    print(
        result[
            [
                "Case_ID",
                "Actual_Pathway",
                "Deviation_Position",
                "Deviation_Activity",
                "Deviation_Type",
            ]
        ].head(12).to_string(index=False)
    )

    result.to_csv(OUTPUT_PATH, index=False)
    summary.to_csv(SUMMARY_PATH, index=False)

    print("\nDetailed analysis saved to:", OUTPUT_PATH)
    print("Summary saved to:", SUMMARY_PATH)
    print("\nDay 16 pathway deviation analysis completed!")