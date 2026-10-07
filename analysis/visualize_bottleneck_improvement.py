"""
CareFlow - Day 20: Visualize Bottleneck Improvement

Visualizes the current versus simulated improved average
duration for non-conforming patient pathways.

This visualization represents a synthetic scenario.
"""

import pandas as pd
import matplotlib.pyplot as plt

INPUT_FILE = "analysis/bottleneck_improvement_simulation.csv"
OUTPUT_FILE = "analysis/bottleneck_improvement_comparison.png"


def visualize_improvement():
    df = pd.read_csv(INPUT_FILE)

    current_duration = df[
        "Current_Average_Duration_Minutes"
    ].iloc[0]

    improved_duration = df[
        "Simulated_Improved_Average_Duration_Minutes"
    ].iloc[0]

    reduction = df[
        "Simulated_Duration_Reduction_Per_Patient"
    ].iloc[0]

    labels = [
        "Current\nNon-Conforming",
        "Simulated\nImproved"
    ]

    values = [
        current_duration,
        improved_duration
    ]

    plt.figure(figsize=(9, 6))

    bars = plt.bar(
        labels,
        values
    )

    plt.title(
        "Bottleneck Improvement Simulation"
    )

    plt.ylabel(
        "Average Pathway Duration (minutes)"
    )

    plt.text(
        0.5,
        max(values) * 0.95,
        f"Modeled reduction: {reduction:.2f} minutes per affected patient",
        ha="center",
        fontsize=11
    )

    for bar, value in zip(bars, values):
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            value + 1,
            f"{value:.2f} min",
            ha="center",
            fontsize=11
        )

    plt.tight_layout()

    plt.savefig(
        OUTPUT_FILE,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("\nBOTTLENECK IMPROVEMENT VISUALIZATION")
    print(f"Current average duration: {current_duration:.2f} minutes")
    print(f"Simulated improved duration: {improved_duration:.2f} minutes")
    print(f"Modeled reduction: {reduction:.2f} minutes per affected patient")

    print("\nVisualization saved to:")
    print(OUTPUT_FILE)

    print("\nDay 21 visualization completed!")


if __name__ == "__main__":
    visualize_improvement()