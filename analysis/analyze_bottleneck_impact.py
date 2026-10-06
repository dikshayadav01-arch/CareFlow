"""
CareFlow - Day 19: Bottleneck Impact Analysis

Analyzes the simulated operational impact of non-conforming
patient pathways using the conformance performance summary.
"""

import pandas as pd

INPUT_FILE = "analysis/conformance_performance_summary.csv"
OUTPUT_FILE = "analysis/bottleneck_impact_analysis.csv"


def analyze_bottleneck_impact():
    df = pd.read_csv(INPUT_FILE)

    conforming = df[
        df["Conformance_Status"] == "CONFORMING"
    ].iloc[0]

    non_conforming = df[
        df["Conformance_Status"] == "NON_CONFORMING"
    ].iloc[0]

    total_patients = int(df["Patient_Count"].sum())

    conforming_avg = conforming["Average_Duration_Minutes"]
    non_conforming_avg = non_conforming["Average_Duration_Minutes"]

    affected_patients = int(non_conforming["Patient_Count"])

    additional_minutes_per_patient = (
        non_conforming_avg - conforming_avg
    )

    total_additional_minutes = (
        additional_minutes_per_patient * affected_patients
    )

    affected_percentage = (
        affected_patients / total_patients
    ) * 100

    potential_reduction_percentage = (
        additional_minutes_per_patient
        / non_conforming_avg
    ) * 100

    results = pd.DataFrame(
        [
            {
                "Total_Patients": total_patients,
                "Affected_Patients": affected_patients,
                "Affected_Patient_Percentage": round(
                    affected_percentage, 2
                ),
                "Conforming_Average_Duration_Minutes": round(
                    conforming_avg, 2
                ),
                "Non_Conforming_Average_Duration_Minutes": round(
                    non_conforming_avg, 2
                ),
                "Additional_Minutes_Per_Affected_Patient": round(
                    additional_minutes_per_patient, 2
                ),
                "Estimated_Total_Additional_Minutes": round(
                    total_additional_minutes, 2
                ),
                "Potential_Duration_Reduction_Percentage": round(
                    potential_reduction_percentage, 2
                ),
            }
        ]
    )

    results.to_csv(OUTPUT_FILE, index=False)

    print("\nBOTTLENECK IMPACT ANALYSIS")
    print(results.to_string(index=False))

    print("\nImportant interpretation:")
    print(
        "The additional time represents an association observed "
        "in the simulated dataset."
    )
    print(
        "It does not establish that pathway deviation caused "
        "the additional duration."
    )

    print("\nAnalysis saved to:")
    print(OUTPUT_FILE)

    print("\nDay 20 bottleneck impact analysis completed!")


if __name__ == "__main__":
    analyze_bottleneck_impact()