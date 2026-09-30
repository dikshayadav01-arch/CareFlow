"""
CareFlow - Conformance Summary

Creates an aggregated summary of conforming
and non-conforming patient pathways.
"""

import pandas as pd

INPUT_PATH = "analysis/conformance_analysis.csv"
OUTPUT_PATH = "analysis/conformance_summary.csv"


def create_summary(df):
    summary = (
        df.groupby(
            ["Expected_Pathway", "Conformance_Status"],
            dropna=False
        )
        .agg(
            Patient_Count=("Patient_ID", "nunique"),
            Average_Activity_Count=("Activity_Count", "mean"),
            Deviation_Count=("Deviation_Flag", "sum"),
        )
        .reset_index()
    )

    summary["Patient_Percentage"] = (
        summary["Patient_Count"]
        / summary["Patient_Count"].sum()
        * 100
    ).round(2)

    summary["Average_Activity_Count"] = (
        summary["Average_Activity_Count"]
        .round(2)
    )

    return summary


if __name__ == "__main__":

    print("CareFlow - Conformance Summary")
    print("-" * 50)

    df = pd.read_csv(INPUT_PATH)

    print("Conformance records:", len(df))

    summary = create_summary(df)

    print("\nConformance Summary")
    print("-" * 50)
    print(summary.to_string(index=False))

    summary.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print("\nSummary saved to:")
    print(OUTPUT_PATH)

    print("\nDay 14 conformance summary completed!")