
"""
CareFlow - Day 17: Patient Pathway Performance Comparison

Compares simulated patient pathway performance using
duration, activity count, conformance status, and deviations.
"""

import pandas as pd

PATHWAY_FILE = "analysis/pathway_analysis.csv"
CONFORMANCE_FILE = "analysis/conformance_impact_analysis.csv"

OUTPUT_FILE = "analysis/pathway_performance_comparison.csv"
STATUS_OUTPUT_FILE = "analysis/conformance_performance_summary.csv"


def compare_pathway_performance():
    # Load existing analysis files
    pathway_df = pd.read_csv(PATHWAY_FILE)
    conformance_df = pd.read_csv(CONFORMANCE_FILE)

    # Select the required conformance fields
    conformance_df = conformance_df[
        [
            "Case_ID",
            "Conformance_Status",
            "Extra_Activities",
            "Deviation_Flag",
        ]
    ]

    # Merge both datasets using Case_ID
    df = pathway_df.merge(
        conformance_df,
        on="Case_ID",
        how="left",
        validate="one_to_one",
    )

    # Check for missing conformance classifications
    if df["Conformance_Status"].isna().any():
        raise ValueError("Some cases have no conformance status.")

    # Performance comparison by pathway and conformance status
    pathway_comparison = (
        df.groupby(["Pathway", "Conformance_Status"])
        .agg(
            Patient_Count=("Case_ID", "count"),
            Average_Duration_Minutes=("Total_Duration_Minutes", "mean"),
            Median_Duration_Minutes=("Total_Duration_Minutes", "median"),
            Minimum_Duration_Minutes=("Total_Duration_Minutes", "min"),
            Maximum_Duration_Minutes=("Total_Duration_Minutes", "max"),
            Average_Activity_Count=("Activity_Count", "mean"),
            Average_Extra_Activities=("Extra_Activities", "mean"),
            Total_Deviations=("Deviation_Flag", "sum"),
        )
        .reset_index()
    )

    # Overall performance comparison by conformance status
    status_comparison = (
        df.groupby("Conformance_Status")
        .agg(
            Patient_Count=("Case_ID", "count"),
            Average_Duration_Minutes=("Total_Duration_Minutes", "mean"),
            Median_Duration_Minutes=("Total_Duration_Minutes", "median"),
            Minimum_Duration_Minutes=("Total_Duration_Minutes", "min"),
            Maximum_Duration_Minutes=("Total_Duration_Minutes", "max"),
            Average_Activity_Count=("Activity_Count", "mean"),
            Average_Extra_Activities=("Extra_Activities", "mean"),
            Total_Deviations=("Deviation_Flag", "sum"),
        )
        .reset_index()
    )

    # Round average and median values for readability
    numeric_columns = [
        "Average_Duration_Minutes",
        "Median_Duration_Minutes",
        "Average_Activity_Count",
        "Average_Extra_Activities",
    ]

    pathway_comparison[numeric_columns] = (
        pathway_comparison[numeric_columns].round(2)
    )
    status_comparison[numeric_columns] = (
        status_comparison[numeric_columns].round(2)
    )

    # Save the output reports
    pathway_comparison.to_csv(OUTPUT_FILE, index=False)
    status_comparison.to_csv(STATUS_OUTPUT_FILE, index=False)

    # Display results
    print("\nPATHWAY PERFORMANCE COMPARISON")
    print(pathway_comparison.to_string(index=False))

    print("\nCONFORMANCE PERFORMANCE SUMMARY")
    print(status_comparison.to_string(index=False))

    print("\nTotal patients analyzed:", len(df))
    print("Pathway comparison saved to:", OUTPUT_FILE)
    print("Conformance summary saved to:", STATUS_OUTPUT_FILE)
    print("\nDay 18 performance comparison completed!")


if __name__ == "__main__":
    compare_pathway_performance()