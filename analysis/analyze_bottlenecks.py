"""
CareFlow - Bottleneck Analysis

Analyzes transitions between patient activities
and calculates the time taken between activities.
"""

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_PATH = "data/raw/ehr_event_log.csv"


# --------------------------------------------------
# Load event log
# --------------------------------------------------

def load_event_log():
    """
    Load the synthetic EHR event log.
    """

    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    return df


# --------------------------------------------------
# Prepare event log
# --------------------------------------------------

def prepare_event_log(df):
    """
    Sort events chronologically within each patient case.
    """

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df

# --------------------------------------------------
# Create activity transitions
# --------------------------------------------------

def create_transitions(df):
    """
    Create transitions between consecutive activities
    and calculate the time between activities.
    """

    transitions = []

    for case_id, case_data in df.groupby("Case_ID"):

        case_data = case_data.sort_values("Timestamp")

        activities = case_data["Activity_Name"].tolist()
        timestamps = case_data["Timestamp"].tolist()

        for i in range(len(activities) - 1):

            duration_minutes = (
                timestamps[i + 1] - timestamps[i]
            ).total_seconds() / 60

            transition = {
                "Case_ID": case_id,
                "From_Activity": activities[i],
                "To_Activity": activities[i + 1],
                "Duration_Minutes": duration_minutes,
            }

            transitions.append(transition)

    return pd.DataFrame(transitions)

# --------------------------------------------------
# Analyze transition statistics
# --------------------------------------------------

def analyze_transition_statistics(transitions):
    """
    Calculate transition frequency and average duration.
    """

    statistics = (
        transitions
        .groupby(
            ["From_Activity", "To_Activity"]
        )
        .agg(
            Transition_Count=("Case_ID", "count"),
            Average_Duration_Minutes=(
                "Duration_Minutes",
                "mean",
            ),
        )
        .reset_index()
    )

    statistics["Average_Duration_Minutes"] = (
        statistics["Average_Duration_Minutes"]
        .round(2)
    )

    statistics = statistics.sort_values(
        by="Transition_Count",
        ascending=False,
    ).reset_index(drop=True)

    return statistics

# --------------------------------------------------
# Analyze X-Ray loop-back
# --------------------------------------------------

def analyze_xray_loopback(transitions):
    """
    Analyze the X-Ray to Triage loop-back transition.
    """

    loopback = transitions[
        (transitions["From_Activity"] == "X-Ray")
        & (transitions["To_Activity"] == "Triage")
    ]

    loopback_count = len(loopback)
    total_transitions = len(transitions)

    loopback_percentage = (
        loopback_count / total_transitions
    ) * 100

    average_loopback_duration = (
        loopback["Duration_Minutes"].mean()
    )

    return (
        loopback_count,
        loopback_percentage,
        average_loopback_duration,
    )

# --------------------------------------------------
# Create bottleneck summary
# --------------------------------------------------

def create_bottleneck_summary(
    transitions,
    statistics,
    loopback_count,
    loopback_percentage,
    average_loopback_duration,
):
    """
    Create a summary of important process bottleneck metrics.
    """

    summary = pd.DataFrame(
        [
            {
                "Metric": "Total Transitions",
                "Value": len(transitions),
            },
            {
                "Metric": "X-Ray to Triage Loop-Backs",
                "Value": loopback_count,
            },
            {
                "Metric": "Loop-Back Percentage of Transitions",
                "Value": round(
                    loopback_percentage,
                    2,
                ),
            },
            {
                "Metric": "Average Loop-Back Duration (Minutes)",
                "Value": round(
                    average_loopback_duration,
                    2,
                ),
            },
            {
                "Metric": "Unique Transition Types",
                "Value": len(statistics),
            },
        ]
    )

    return summary

# --------------------------------------------------
# Main execution
# --------------------------------------------------

if __name__ == "__main__":

    print("CareFlow - Bottleneck Analysis")
    print("-" * 40)

    df = load_event_log()

    print("Events loaded:", len(df))
    print("Cases loaded:", df["Case_ID"].nunique())

    df = prepare_event_log(df)

    print("\nEvent log prepared successfully!")

    transitions = create_transitions(df)

    print("\nTransitions created:", len(transitions))

    print("\nFirst 10 transitions:")
    print(
        transitions.head(10).to_string(index=False)
    )

    statistics = analyze_transition_statistics(
        transitions
    )

    print("\nTransition Statistics")
    print("---------------------")

    print(
        statistics.to_string(index=False)
    )

    (
        loopback_count,
        loopback_percentage,
        average_loopback_duration,
    ) = analyze_xray_loopback(transitions)

    print("\nX-Ray Loop-Back Analysis")
    print("------------------------")

    print(
        "X-Ray → Triage transitions:",
        loopback_count,
    )

    print(
        "Loop-back percentage:",
        round(loopback_percentage, 2),
        "%",
    )

    print(
        "Average loop-back duration:",
        round(average_loopback_duration, 2),
        "minutes",
    )

    summary = create_bottleneck_summary(
        transitions,
        statistics,
        loopback_count,
        loopback_percentage,
        average_loopback_duration,
    )

    print("\nBottleneck Summary")
    print("------------------")

    print(
        summary.to_string(index=False)
    )

    output_path = "analysis/transition_analysis.csv"

    transitions.to_csv(
        output_path,
        index=False,
    )

    print("\nTransition analysis saved to:")
    print(output_path)

    print("\nEvent log prepared successfully!")

    print("\nFirst 10 events:")
    print(df.head(10).to_string(index=False))