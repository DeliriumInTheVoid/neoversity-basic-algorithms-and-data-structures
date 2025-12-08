import networkx as nx
import heapq
from typing import Dict, Tuple, List


def paths_dijkstra(graph: nx.Graph, start: str) -> Dict[str, Tuple[float, List[str]]]:
    distances = {node: (float('inf'), []) for node in graph.nodes}
    distances[start] = (0, [start])
    priority_queue = [(0, start, [start])]

    while priority_queue:
        current_distance, current_node, path = heapq.heappop(priority_queue)

        if current_distance > distances[current_node][0]:
            continue

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get('weight', 1)
            distance = current_distance + weight
            if distance < distances[neighbor][0]:
                distances[neighbor] = (distance, path + [neighbor])
                heapq.heappush(priority_queue, (distance, neighbor, path + [neighbor]))

    return distances
