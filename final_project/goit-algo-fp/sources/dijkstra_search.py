import heapq
import matplotlib.pyplot as plt
import networkx as nx
import random

from typing import Any, Dict, Iterable, List, Optional, Tuple


def paths_dijkstra(graph: nx.Graph, start: str) -> Dict[str, Tuple[float, List[str]]]:
    """
    Dijkstra (binary heap) that returns for each node:
      (shortest_distance_from_start, path_as_list_of_nodes)

    Notes:
    - Works for nx.Graph and nx.DiGraph.
    - Requires non-negative edge weights.
    - Uses "lazy deletion" for heap entries (skip outdated distances).
    - Avoids pushing full paths into the heap (stores predecessors instead).
    """
    if start not in graph:
        raise KeyError(f"Start node {start!r} is not in the graph.")

    # dijkstra requires non-negative weights
    for u, v, data in graph.edges(data=True):
        w = data.get("weight", 1)
        if w < 0:
            raise ValueError("Dijkstra's algorithm requires non-negative edge weights.")

    dist: Dict[str, float] = {node: float("inf") for node in graph.nodes}
    prev: Dict[str, str | None] = {node: None for node in graph.nodes}

    dist[start] = 0.0
    heap: List[Tuple[float, str]] = [(0.0, start)]  # (distance, node)

    while heap:
        current_dist, u = heapq.heappop(heap)

        if current_dist != dist[u]:
            continue

        for v in graph.neighbors(u):
            w = graph[u][v].get("weight", 1)
            cand = current_dist + w
            if cand < dist[v]:
                dist[v] = cand
                prev[v] = u
                heapq.heappush(heap, (cand, v))

    def build_path(target: str) -> List[str]:
        if dist[target] == float("inf"):
            return []
        path: List[str] = []
        cur: str | None = target
        while cur is not None:
            path.append(cur)
            cur = prev[cur]
        path.reverse()
        return path

    return {node: (dist[node], build_path(node)) for node in graph.nodes}


def draw_graph_with_path(
    graph: nx.Graph,
    path: Optional[List[Any]] = None,
    *,
    pos: Optional[Dict[Any, Tuple[float, float]]] = None,
    title: Optional[str] = None,
    show_weights: bool = True,
    seed: int = 42,
    ax: Optional[plt.Axes] = None,
) -> Dict[Any, Tuple[float, float]]:
    """
    Draw a NetworkX graph with an optional highlighted path.

    Parameters
    ----------
    graph : nx.Graph | nx.DiGraph
        Weighted graph. Edge weight is read from 'weight' attribute (defaults to 1 if missing).
    path : list[Any] | None
        Node sequence representing a path to highlight, e.g. ["A","C","B","D"].
    pos : dict | None
        Precomputed layout positions. If None, spring_layout is used.
    title : str | None
        Plot title.
    show_weights : bool
        If True, show edge weight labels.
    seed : int
        Random seed for spring_layout (only used if pos is None).
    ax : matplotlib.axes.Axes | None
        If provided, draw onto this axes; otherwise a new figure/axes is created.

    Returns
    -------
    pos : dict
        Positions used for drawing (can be reused for consistent layout).
    """
    if graph.is_multigraph():
        raise NotImplementedError("This helper currently supports only Graph/DiGraph, not MultiGraph/MultiDiGraph.")

    if ax is None:
        _, ax = plt.subplots(figsize=(9, 6))

    if pos is None:
        pos = nx.spring_layout(graph, seed=seed)

    base_node_color = "#E6E6E6"
    base_edge_color = "#B0B0B0"

    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=900, node_color=base_node_color, edgecolors="#404040")
    nx.draw_networkx_edges(graph, pos, ax=ax, width=1.5, edge_color=base_edge_color, arrows=graph.is_directed())
    nx.draw_networkx_labels(graph, pos, ax=ax, font_size=10)

    if show_weights:
        edge_labels = {}
        for u, v, data in graph.edges(data=True):
            edge_labels[(u, v)] = data.get("weight", 1)
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax, font_size=9)

    if path and len(path) >= 2:
        path_nodes = list(dict.fromkeys(path))  # preserve order, remove duplicates if any
        path_edges = list(zip(path, path[1:]))

        # nodes on the path
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=path_nodes,
            ax=ax,
            node_size=980,
            node_color="#FFD166",
            edgecolors="#8A5A00",
        )

        # edges on the path
        nx.draw_networkx_edges(
            graph,
            pos,
            edgelist=path_edges,
            ax=ax,
            width=4.0,
            edge_color="#EF476F",
            arrows=graph.is_directed(),
        )

        # start/end nodes
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=[path[0]],
            ax=ax,
            node_size=1050,
            node_color="#06D6A0",
            edgecolors="#006B4F",
        )
        nx.draw_networkx_nodes(
            graph,
            pos,
            nodelist=[path[-1]],
            ax=ax,
            node_size=1050,
            node_color="#118AB2",
            edgecolors="#0B4F66",
        )

    ax.set_title(title or "Graph with highlighted path")
    ax.axis("off")
    plt.tight_layout()
    plt.show()
    return pos


def create_transportation_network(num_stations: int, num_connections: int, weights: bool = False) -> nx.Graph:
    graph = nx.Graph()

    for i in range(num_stations):
        graph.add_node(f"S_{i+1}")

    while graph.number_of_edges() < num_connections:
        station_a = f"S_{random.randint(1, num_stations)}"
        station_b = f"S_{random.randint(1, num_stations)}"
        if station_a != station_b:
            graph.add_edge(station_a, station_b, weight=random.randint(1, 10) if weights else 1)

    return graph


if __name__ == "__main__":
    G = create_transportation_network(num_stations=10, num_connections=20, weights=True)
    start, target = "S_1", "S_7"

    result = paths_dijkstra(G, start)
    for node, (d, p) in result.items():
        print(f"{start} -> {node}: distance={d}, path={p}")

    dist, path = result[target]

    print(f"Shortest path {start} -> {target}: {path}, distance={dist}")
    draw_graph_with_path(G, path, title=f"Shortest path {start} -> {target} (distance={dist})")

