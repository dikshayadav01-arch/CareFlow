"""
CareFlow - Day 20: Bottleneck Improvement Simulation

Simulates the potential operational impact if non-conforming
patient pathways performed at the average duration of
conforming pathways.

This is a synthetic scenario analysis and does not establish
causation or predict real-world hospital outcomes.
"""

import pandas as pd

INPUT_FILE = "analysis/conformance_performance_summary.csv"
OUTPUT_FILE = "analysis/bottleneck_improvement_simulation.csv"


def simulate_improvement():
    df = pd.read_csv(INPUT_FILE)

    conforming = df[
        df["Conformance_Status"] == "CONFORMING"
    ].iloc[0]

    non_conforming = df[
        df["Conformance_Status"] == "NON_CONFORMING"
    ].iloc[0]

    total_patients = int(df["Patient_Count"].sum())

    affected_patients = int(
        non_conforming["Patient_Count"]
    )

    current_non_conforming_duration = (
        non_conforming["Average_Duration_Minutes"]
    )

    simulated_improved_duration = (
        conforming["Average_Duration_Minutes"]
    )

    duration_reduction_per_patient = (
        current_non_conforming_duration
        - simulated_improved_duration
    )

    current_total_duration = (
        current_non_conforming_duration
        * affected_patients
    )

    simulated_total_duration = (
        simulated_improved_duration
        * affected_patients
    )

    total_simulated_time_reduction = (
        current_total_duration
        - simulated_total_duration
    )

    affected_percentage = (
        affected_patients / total_patients
    ) * 100

    reduction_percentage = (
        duration_reduction_per_patient
        / current_non_conforming_duration
    ) * 100

    results = pd.DataFrame(
        [
            {
                "Total_Patients": total_patients,
                "Affected_Patients": affected_patients,
                "Affected_Patient_Percentage": round(
                    affected_percentage, 2
                ),
                "Current_Average_Duration_Minutes": round(
                    current_non_conforming_duration, 2
                ),
                "Simulated_Improved_Average_Duration_Minutes": round(
                    simulated_improved_duration, 2
                ),
                "Simulated_Duration_Reduction_Per_Patient": round(
                    duration_reduction_per_patient, 2
                ),
                "Current_Total_Duration_Minutes": round(
                    current_total_duration, 2
                ),
                "Simulated_Total_Duration_Minutes": round(
                    simulated_total_duration, 2
                ),
                "Total_Simulated_Time_Reduction_Minutes": round(
                    total_simulated_time_reduction, 2
                ),
                "Simulated_Reduction_Percentage": round(
                    reduction_percentage, 2
                ),
            }
        ]
    )

    results.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("\nBOTTLENECK IMPROVEMENT SIMULATION")
    print(results.to_string(index=False))

    print("\nScenario interpretation:")
    print(
        "This simulation assumes that affected patient "
        "pathways could perform at the average duration "
        "observed for conforming pathways."
    )

    print(
        "The result represents a modeled scenario using "
        "synthetic data and is not a causal or real-world "
        "hospital improvement estimate."
    )

    print("\nAnalysis saved to:")
    print(OUTPUT_FILE)

    print("\nDay 21 bottleneck improvement simulation completed!")


if __name__ == "__main__":
    simulate_improvement()