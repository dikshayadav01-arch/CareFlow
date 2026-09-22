"""
CareFlow - Process Flow Graph

Creates a directed process graph from the
patient activity transition analysis.
"""

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt


# --------------------------------------------------
# Configuration
# --------------------------------------------------

INPUT_PATH = "analysis/transition_analysis.csv"
OUTPUT_PATH = "analysis/process_flow_graph.png"


# --------------------------------------------------
# Load transition analysis
# --------------------------------------------------

def load_transition_data():
    """
    Load transition-level analysis data.
    """

    df = pd.read_csv(INPUT_PATH)

    return df


# --------------------------------------------------
# Create process graph
# --------------------------------------------------

def create_process_graph(df):
    """
    Create a directed graph from patient activity
    transitions.
    """

    graph = nx.DiGraph()

    for _, row in df.iterrows():

        from_activity = row["From_Activity"]
        to_activity = row["To_Activity"]

        if graph.has_edge(
            from_activity,
            to_activity,
        ):

            graph[from_activity][to_activity][
                "weight"
            ] += 1

        else:

            graph.add_edge(
                from_activity,
                to_activity,
                weight=1,
            )

    return graph

# --------------------------------------------------
# Visualize process graph
# --------------------------------------------------

def visualize_process_graph(graph):
    """
    Create and save a visual representation
    of the patient process flow.

    The X-Ray to Triage loop-back is highlighted
    separately because it represents the simulated
    bottleneck.
    """

    plt.figure(figsize=(14, 9))

    positions = nx.spring_layout(
        graph,
        seed=42,
        k=2.0,
    )

    # ----------------------------------------------
    # Draw nodes
    # ----------------------------------------------

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=3000,
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=10,
        font_weight="bold",
    )

    # ----------------------------------------------
    # Separate normal and loop-back edges
    # ----------------------------------------------

    normal_edges = []
    loopback_edges = []

    for source, target in graph.edges():

        if (
            source == "X-Ray"
            and target == "Triage"
        ):
            loopback_edges.append(
                (source, target)
            )
        else:
            normal_edges.append(
                (source, target)
            )

    # ----------------------------------------------
    # Draw normal transitions
    # ----------------------------------------------

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=normal_edges,
        arrows=True,
        arrowsize=20,
        width=2,
        connectionstyle="arc3,rad=0.08",
    )

    # ----------------------------------------------
    # Draw bottleneck transition
    # ----------------------------------------------

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=loopback_edges,
        arrows=True,
        arrowsize=25,
        width=4,
        edge_color="red",
        connectionstyle="arc3,rad=0.15",
    )

    # ----------------------------------------------
    # Draw transition counts
    # ----------------------------------------------

    edge_labels = nx.get_edge_attributes(
        graph,
        "weight",
    )

    nx.draw_networkx_edge_labels(
        graph,
        positions,
        edge_labels=edge_labels,
        font_size=9,
    )

    # ----------------------------------------------
    # Title
    # ----------------------------------------------

    plt.title(
    "CareFlow Patient Process Flow\n"
    "Highlighted X-Ray → Triage Loop-Back",
    fontsize=16,
    )

    plt.text(
    0.02,
    0.02,
    "Bottleneck: X-Ray → Triage\n"
    "Loop-backs: 16\n"
    "Average duration: 20.19 minutes",
    transform=plt.gca().transAxes,
    fontsize=11,
    verticalalignment="bottom",
    bbox=dict(
        boxstyle="round,pad=0.5",
        facecolor="white",
        edgecolor="black",
    ),
)

    plt.axis("off")

    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    return OUTPUT_PATH

# --------------------------------------------------
# Main execution
# --------------------------------------------------

if __name__ == "__main__":

    print("CareFlow - Process Flow Graph")
    print("-" * 40)

    df = load_transition_data()

    print("Transitions loaded:", len(df))

    graph = create_process_graph(df)

    print("Graph created successfully!")

    print("Nodes:", graph.number_of_nodes())
    print("Edges:", graph.number_of_edges())

    print("\nProcess transitions:")

    for source, target, data in graph.edges(data=True):

        print(
            f"{source} -> {target} "
            f"(count: {data['weight']})"
        )

    output_path = visualize_process_graph(
        graph
    )

    print("\nProcess graph saved to:")
    print(output_path)    