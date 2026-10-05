"""
CareFlow - Day 18: Patient Pathway Performance Visualization

Creates visualizations for simulated patient pathway performance
using the Day 17 analysis results.
"""

import pandas as pd
import matplotlib.pyplot as plt


PATHWAY_FILE = "analysis/pathway_performance_comparison.csv"
CONFORMANCE_FILE = "analysis/conformance_performance_summary.csv"

DURATION_OUTPUT = "analysis/pathway_duration_comparison.png"
ACTIVITY_OUTPUT = "analysis/activity_count_comparison.png"
PATIENT_OUTPUT = "analysis/conformance_patient_count.png"


def load_data():
    pathway_df = pd.read_csv(PATHWAY_FILE)
    conformance_df = pd.read_csv(CONFORMANCE_FILE)

    return pathway_df, conformance_df


def create_duration_chart(pathway_df):
    plt.figure(figsize=(10, 6))

    plt.bar(
        pathway_df["Pathway"],
        pathway_df["Average_Duration_Minutes"],
    )

    plt.title(
        "CareFlow - Average Patient Pathway Duration",
        fontsize=15,
        fontweight="bold",
    )

    plt.xlabel("Patient Pathway")
    plt.ylabel("Average Duration (Minutes)")

    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        DURATION_OUTPUT,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("Saved:", DURATION_OUTPUT)


def create_activity_chart(pathway_df):
    plt.figure(figsize=(10, 6))

    plt.bar(
        pathway_df["Pathway"],
        pathway_df["Average_Activity_Count"],
    )

    plt.title(
        "CareFlow - Average Activities per Patient Pathway",
        fontsize=15,
        fontweight="bold",
    )

    plt.xlabel("Patient Pathway")
    plt.ylabel("Average Activity Count")

    plt.xticks(rotation=15)
    plt.tight_layout()

    plt.savefig(
        ACTIVITY_OUTPUT,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("Saved:", ACTIVITY_OUTPUT)


def create_conformance_patient_chart(conformance_df):
    plt.figure(figsize=(8, 6))

    plt.bar(
        conformance_df["Conformance_Status"],
        conformance_df["Patient_Count"],
    )

    plt.title(
        "CareFlow - Patients by Conformance Status",
        fontsize=15,
        fontweight="bold",
    )

    plt.xlabel("Conformance Status")
    plt.ylabel("Patient Count")

    plt.tight_layout()

    plt.savefig(
        PATIENT_OUTPUT,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("Saved:", PATIENT_OUTPUT)


def main():
    pathway_df, conformance_df = load_data()

    print("\nCreating Day 19 visualizations...\n")

    create_duration_chart(pathway_df)
    create_activity_chart(pathway_df)
    create_conformance_patient_chart(conformance_df)

    print("\nDay 19 visualization completed successfully!")


if __name__ == "__main__":
    main()