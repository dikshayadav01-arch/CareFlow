
from pathlib import Path

import pandas as pd
import pm4py
from pm4py.visualization.process_tree import visualizer as pt_visualizer

# Resolve paths independently of the current working directory.
PROJECT_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = PROJECT_DIR / "data" / "raw" / "ehr_event_log.csv"
PROCESSED_DIR = PROJECT_DIR / "data" / "processed"
OUTPUT_PATH = PROCESSED_DIR / "ehr_event_log_prepared.csv"
VARIANTS_PATH = PROCESSED_DIR / "process_variants.csv"
TREE_PATH = PROJECT_DIR / "process_mining" / "process_tree.png"

REQUIRED_COLUMNS = {
    "Case_ID",
    "Activity_Name",
    "Timestamp",
}


def load_event_log():
    """Load the synthetic EHR event log and validate its schema."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Input event log not found: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")

    if df.empty:
        raise ValueError("The input event log is empty.")

    if df[list(REQUIRED_COLUMNS)].isna().any().any():
        raise ValueError("Required case, activity, or timestamp values are missing.")

    return df


def prepare_event_log(df):
    """Parse timestamps and sort events chronologically within each case."""
    df = df.copy()
    df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="raise")
    return df.sort_values(
        ["Case_ID", "Timestamp"]
    ).reset_index(drop=True)


def convert_to_pm4py(df):
    """Convert the prepared DataFrame into a PM4Py event log."""
    return pm4py.format_dataframe(
        df.copy(),
        case_id="Case_ID",
        activity_key="Activity_Name",
        timestamp_key="Timestamp",
    )



def analyze_variants(event_log):
    """Return process variants and their case counts."""
    variants = pm4py.get_variants(event_log)

    rows = [
        {
            "Variant": " -> ".join(str(activity) for activity in variant),
            "Case_Count": count,
        }
        for variant, count in variants.items()
    ]

    return pd.DataFrame(
        rows,
        columns=["Variant", "Case_Count"],
    ).sort_values(
        "Case_Count",
        ascending=False,
    ).reset_index(drop=True)



def discover_process_model(event_log):
    """Discover a process tree using the Inductive Miner."""
    return pm4py.discover_process_tree_inductive(event_log)


def visualize_process_model(process_tree):
    """Save the discovered process tree as a PNG image."""
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    gviz = pt_visualizer.apply(process_tree)
    pt_visualizer.save(gviz, str(TREE_PATH))

    return TREE_PATH


def main():
    print("=" * 60)
    print("CAREFLOW - PROCESS MINING PIPELINE")
    print("=" * 60)

    df = prepare_event_log(load_event_log())

    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUTPUT_PATH, index=False)

    event_log = convert_to_pm4py(df)
    variants_df = analyze_variants(event_log)
    variants_df.to_csv(VARIANTS_PATH, index=False)

    process_tree = discover_process_model(event_log)
    tree_path = visualize_process_model(process_tree)

    print(f"\nInput events: {len(df)}")
    print(f"Unique cases: {df['Case_ID'].nunique()}")
    print(f"Unique activities: {df['Activity_Name'].nunique()}")
    print(f"Unique process variants: {len(variants_df)}")
    print(f"\nVariant summary:\n{variants_df.to_string(index=False)}")

    print("\nGenerated outputs:")
    print(f"Prepared event log: {OUTPUT_PATH}")
    print(f"Process variants:   {VARIANTS_PATH}")
    print(f"Process tree:       {tree_path}")
    print("\nPROCESS-MINING PIPELINE COMPLETED SUCCESSFULLY.")


if __name__ == "__main__":
    main()
