"""
CareFlow - Process Mining Event Log Preparation

Loads the synthetic EHR event log and prepares it
for PM4Py process mining analysis.
"""

import pandas as pd
import pm4py
from pm4py.visualization.process_tree import visualizer as pt_visualizer

# Configuration

INPUT_PATH = "data/raw/ehr_event_log.csv"

# Load event log

def load_event_log():
   
    """
    Load the synthetic EHR event log from CSV.
    """

    df = pd.read_csv(INPUT_PATH)

    return df

# Prepare event log

def prepare_event_log(df):

    """
    Convert timestamp values and sort events
    into chronological order for each case.
    """

    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    df = df.sort_values(
        by=["Case_ID", "Timestamp"]
    ).reset_index(drop=True)

    return df 

# Convert to PM4Py event log

def convert_to_pm4py(df):
    """
    Convert the prepared Pandas DataFrame
    into a PM4Py event log.
    """

    event_log = pm4py.format_dataframe(
        df,
        case_id="Case_ID",
        activity_key="Activity_Name",
        timestamp_key="Timestamp",
    )

    return event_log

# Analyze process variants

def analyze_variants(event_log):
    
    """
    Identify unique patient journey variants
    and count how many cases follow each variant.
    """

    variants = pm4py.get_variants(event_log)

    return variants

# Discover process model

def discover_process_model(event_log):
    """
    Discover a process model from the event log
    using PM4Py's Inductive Miner.
    """

    process_tree = pm4py.discover_process_tree_inductive(
        event_log
    )

    return process_tree

# Visualize process model

def visualize_process_model(process_tree):
    """
    Generate a visual representation of the
    discovered process tree.
    """

    gviz = pt_visualizer.apply(process_tree)

    output_path = "process_mining/process_tree.png"

    pt_visualizer.save(
        gviz,
        output_path,
    )

    return output_path

# Main execution

if __name__ == "__main__":

    print("CareFlow - Process Mining Preparation")
    print("-" * 45)

    df = load_event_log()

    print("Raw events:", len(df))
    print("Cases:", df["Case_ID"].nunique())

    df = prepare_event_log(df)

    print("\nPrepared event log")
    print("------------------")
    print("Events:", len(df))
    print("Cases:", df["Case_ID"].nunique())
    print("Timestamp type:", df["Timestamp"].dtype)

    event_log = convert_to_pm4py(df)

    print("\nPM4Py event log")
    print("----------------")
    print("Events:", len(event_log))
    print("Cases:", event_log["case:concept:name"].nunique())
    print("Activities:", event_log["concept:name"].nunique())

    print("\nActivity names:")
    print(
        sorted(
            event_log["concept:name"].unique()
        )
    )

    variants = analyze_variants(event_log)

    print("\nProcess variants")
    print("----------------")

    for variant, count in variants.items():
        print(f"{count} cases: {variant}")

    print("\nUnique process variants:", len(variants))

    process_tree = discover_process_model(event_log)

    print("\nProcess model discovered successfully!")
    print("Process tree:")
    print(process_tree)

    output_path = visualize_process_model(process_tree)

    print("\nProcess visualization saved to:")
    print(output_path)

    print("\nPM4Py conversion completed successfully!")