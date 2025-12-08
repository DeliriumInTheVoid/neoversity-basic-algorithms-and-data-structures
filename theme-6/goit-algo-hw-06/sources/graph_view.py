import networkx as nx
import matplotlib.pyplot as plt

def analyze_graph(graph: nx.Graph):
    num_vertices = graph.number_of_nodes()
    num_edges = graph.number_of_edges()
    degrees = dict(graph.degree())

    print(f"Number of vertices (stations): {num_vertices}")
    print(f"Number of edges (connections): {num_edges}")
    print("Degree of each vertex (station):")
    for station, degree in degrees.items():
        print(f"  {station}: {degree}")

    print(f"\nEdges in the graph:")
    for edge in graph.edges():
        print(f"  {edge[0]} <-> {edge[1]}")


def visualize_graph(graph: nx.Graph):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, node_size=700, node_color="lightblue", font_size=10, font_weight="bold", edge_color="gray")
    plt.title("Transportation Network Graph")
    plt.show()

