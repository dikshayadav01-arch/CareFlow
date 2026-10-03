
"""
CareFlow - Patient Pathway Deviation Visualization

Visualizes ideal and simulated loop-back patient pathways.
"""

import matplotlib.pyplot as plt
import networkx as nx

OUTPUT_PATH = "analysis/pathway_deviation_graph.png"


def create_pathway_graph():
    graph = nx.DiGraph()

    # Ideal patient pathway
    ideal_edges = [
        ("Registration", "Triage"),
        ("Triage", "Doctor Consultation"),
        ("Doctor Consultation", "X-Ray"),
        ("X-Ray", "Treatment"),
        ("Treatment", "Discharge"),
    ]

    # Additional simulated loop-back transitions
    loopback_edges = [
        ("X-Ray", "Triage"),
        ("Triage", "Doctor Consultation"),
    ]

    graph.add_edges_from(ideal_edges)
    graph.add_edges_from(loopback_edges)

    return graph, ideal_edges, loopback_edges


def visualize_pathway():
    graph, ideal_edges, loopback_edges = (
        create_pathway_graph()
    )

    positions = {
        "Registration": (0, 0),
        "Triage": (1.5, 0),
        "Doctor Consultation": (3.2, 0),
        "X-Ray": (5, 0),
        "Treatment": (6.8, 0),
        "Discharge": (8.5, 0),
    }

    plt.figure(figsize=(16, 7))

    nx.draw_networkx_nodes(
        graph,
        positions,
        node_size=3300,
        node_color="lightblue",
        edgecolors="black",
    )

    nx.draw_networkx_labels(
        graph,
        positions,
        font_size=9,
        font_weight="bold",
    )

    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=ideal_edges,
        edge_color="steelblue",
        width=2.5,
        arrows=True,
        arrowsize=20,
        connectionstyle="arc3,rad=0.0",
    )

    # Highlight the simulated loop-back
    nx.draw_networkx_edges(
        graph,
        positions,
        edgelist=[("X-Ray", "Triage")],
        edge_color="red",
        width=3,
        style="dashed",
        arrows=True,
        arrowsize=22,
        connectionstyle="arc3,rad=0.35",
    )

    plt.text(
        3.2,
        1.65,
        "Simulated loop-back:\nX-Ray → Triage → Doctor Consultation",
        fontsize=11,
        color="red",
        ha="center",
        fontweight="bold",
    )

    plt.title(
        "CareFlow - Patient Pathway Deviation Analysis",
        fontsize=16,
        fontweight="bold",
    )

    plt.text(
        4.2,
        -1.25,
        "84 conforming patients | 16 simulated loop-back patients",
        ha="center",
        fontsize=11,
    )

    plt.axis("off")
    plt.tight_layout()

    plt.savefig(
        OUTPUT_PATH,
        dpi=300,
        bbox_inches="tight",
    )

    plt.close()

    print("Pathway deviation visualization saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    visualize_pathway()
    print("Day 17 pathway visualization completed!")