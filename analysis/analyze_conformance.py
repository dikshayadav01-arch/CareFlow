"""
CareFlow - Conformance Checking

Compares actual synthetic patient pathways
against predefined ideal pathways.
"""

import pandas as pd

INPUT_PATH = "data/raw/ehr_event_log.csv"
OUTPUT_PATH = "analysis/conformance_analysis.csv"


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
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)


def compare_pathway(actual_activities):
    actual = list(actual_activities)

    for pathway_name, ideal in IDEAL_PATHWAYS.items():
        if actual == ideal:
            return pathway_name, "CONFORMING", 0

    loopback_pattern = [
        "Registration",
        "Triage",
        "Doctor Consultation",
        "X-Ray",
        "Triage",
        "Doctor Consultation",
        "Treatment",
        "Discharge",
    ]

    if actual == loopback_pattern:
        return "XRAY_LOOPBACK", "NON_CONFORMING", 1

    return "UNKNOWN", "NON_CONFORMING", 1


def analyze_conformance(df):
    records = []

    for case_id, case_data in df.groupby("Case_ID"):
        case_data = case_data.sort_values("Timestamp")

        activities = case_data["Activity_Name"].tolist()

        expected_pathway, status, deviation_count = (
            compare_pathway(activities)
        )

        records.append({
            "Case_ID": case_id,
            "Patient_ID": case_data["Patient_ID"].iloc[0],
            "Actual_Pathway": " -> ".join(activities),
            "Expected_Pathway": expected_pathway,
            "Conformance_Status": status,
            "Deviation_Flag": deviation_count,
            "Activity_Count": len(activities),
        })

    return pd.DataFrame(records)


if __name__ == "__main__":

    print("CareFlow - Conformance Checking")
    print("-" * 50)

    df = load_event_log()

    print("Events loaded:", len(df))
    print("Cases loaded:", df["Case_ID"].nunique())

    result = analyze_conformance(df)

    print("\nConformance Status")
    print("-" * 50)
    print(
        result["Conformance_Status"]
        .value_counts()
        .to_string()
    )

    print("\nDeviation Count")
    print("-" * 50)
    print(
        result["Deviation_Flag"]
        .value_counts()
        .sort_index()
        .to_string()
    )

    print("\nSample Results")
    print("-" * 50)
    print(
        result[
            [
                "Case_ID",
                "Expected_Pathway",
                "Conformance_Status",
                "Deviation_Flag",
                "Activity_Count",
            ]
        ].head(10).to_string(index=False)
    )

    result.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nConformance analysis saved to:")
    print(OUTPUT_PATH)

    print("\nDay 14 conformance analysis completed!")