import networkx as nx

from collections import deque


def bfs(graph: nx.Graph, start: str, goal: str):
    visited = set()
    queue = deque([(start, [start])])
    visited.add(start)  # start as visited immediately

    while queue:
        current_node, path = queue.popleft()
        if current_node == goal:
            return path

        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    return None


def dfs(graph: nx.Graph, start: str, goal: str, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    visited.add(start)
    path.append(start)

    if start == goal:
        return path

    for neighbor in graph.neighbors(start):
        if neighbor not in visited:
            result = dfs(graph, neighbor, goal, visited, path)
            if result is not None:
                return result

    path.pop()
    return None
