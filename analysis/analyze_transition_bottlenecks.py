"""
CareFlow - Transition Bottleneck Analysis

Analyzes the time spent between consecutive patient
activities and identifies high-duration transitions.
"""

import pandas as pd


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_PATH = "data/raw/ehr_event_log.csv"

OUTPUT_PATH = (
    "analysis/transition_bottleneck_analysis.csv"
)


# --------------------------------------------------
# Load event log
# --------------------------------------------------

def load_event_log():
    """
    Load and prepare the synthetic EHR event log.
    """

    df = pd.read_csv(INPUT_PATH)

    df["Timestamp"] = pd.to_datetime(
        df["Timestamp"]
    )

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df


# --------------------------------------------------
# Create transitions
# --------------------------------------------------

def create_transitions(df):
    """
    Create consecutive activity transitions
    for every patient case.
    """

    transitions = []

    for case_id, case_data in df.groupby(
        "Case_ID"
    ):

        case_data = case_data.sort_values(
            "Timestamp"
        )

        activities = case_data[
            "Activity_Name"
        ].tolist()

        timestamps = case_data[
            "Timestamp"
        ].tolist()

        for i in range(
            len(activities) - 1
        ):

            duration_minutes = (
                timestamps[i + 1]
                - timestamps[i]
            ).total_seconds() / 60

            transitions.append(
                {
                    "Case_ID": case_id,
                    "From_Activity": activities[i],
                    "To_Activity": activities[i + 1],
                    "Duration_Minutes": round(
                        duration_minutes,
                        2,
                    ),
                }
            )

    return pd.DataFrame(transitions)


# --------------------------------------------------
# Analyze transition statistics
# --------------------------------------------------

def analyze_transitions(transitions):
    """
    Calculate statistics for each unique transition.
    """

    summary = (
        transitions
        .groupby(
            [
                "From_Activity",
                "To_Activity",
            ]
        )
        .agg(
            Transition_Count=(
                "Duration_Minutes",
                "count",
            ),
            Average_Duration_Minutes=(
                "Duration_Minutes",
                "mean",
            ),
            Minimum_Duration_Minutes=(
                "Duration_Minutes",
                "min",
            ),
            Maximum_Duration_Minutes=(
                "Duration_Minutes",
                "max",
            ),
        )
        .reset_index()
    )

    summary[
        "Average_Duration_Minutes"
    ] = summary[
        "Average_Duration_Minutes"
    ].round(2)

    return summary


# --------------------------------------------------
# Calculate total transition time
# --------------------------------------------------

def calculate_total_transition_time(
    summary
):
    """
    Calculate the total observed transition time
    represented by each transition type.
    """

    summary[
        "Estimated_Total_Duration_Minutes"
    ] = (
        summary["Transition_Count"]
        * summary["Average_Duration_Minutes"]
    ).round(2)

    return summary


# --------------------------------------------------
# Rank bottlenecks
# --------------------------------------------------

def rank_bottlenecks(summary):
    """
    Rank transitions by average duration.
    """

    ranked = summary.sort_values(
        by="Average_Duration_Minutes",
        ascending=False,
    ).reset_index(drop=True)

    ranked.insert(
        0,
        "Duration_Rank",
        range(1, len(ranked) + 1),
    )

    return ranked

# --------------------------------------------------
# Analyze loop-back impact
# --------------------------------------------------

def analyze_loopback_impact(transitions):
    """
    Analyze the X-Ray -> Triage loop-back transition.
    """

    loopback = transitions[
        (transitions["From_Activity"] == "X-Ray")
        & (transitions["To_Activity"] == "Triage")
    ]

    loopback_count = len(loopback)

    if loopback_count > 0:
        average_duration = round(
            loopback["Duration_Minutes"].mean(),
            2,
        )

        total_duration = round(
            loopback["Duration_Minutes"].sum(),
            2,
        )
    else:
        average_duration = 0
        total_duration = 0

    return {
        "Loopback_Count": loopback_count,
        "Average_Loopback_Duration_Minutes": average_duration,
        "Total_Loopback_Duration_Minutes": total_duration,
    }

# --------------------------------------------------
# Main execution
# --------------------------------------------------

if __name__ == "__main__":

    print(
        "CareFlow - Transition Bottleneck Analysis"
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

    transitions = create_transitions(
        df
    )

    print(
        "\nTransitions created:",
        len(transitions)
    )

    summary = analyze_transitions(
        transitions
    )

    summary = calculate_total_transition_time(
        summary
    )

    ranked = rank_bottlenecks(
        summary
    )

    loopback_impact = analyze_loopback_impact(
        transitions
    )

    print(
        "\nTransition bottleneck ranking"
    )

    print("-" * 50)

    print(
        ranked.to_string(
            index=False
        )
    )

    print(
    "\nX-Ray -> Triage loop-back impact"
)

    print("-" * 50)

    print(
    "Loop-back count:",
    loopback_impact["Loopback_Count"]
)

    print(
    "Average loop-back duration:",
    loopback_impact[
        "Average_Loopback_Duration_Minutes"
    ],
    "minutes"
)

    print(
    "Total loop-back duration:",
    loopback_impact[
        "Total_Loopback_Duration_Minutes"
    ],
    "minutes"
)

    ranked.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(
        "\nBottleneck analysis saved to:"
    )

    print(
        OUTPUT_PATH
    )

    print(
        "\nDay 8 transition analysis completed!"
    )