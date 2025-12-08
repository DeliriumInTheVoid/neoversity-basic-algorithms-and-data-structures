import networkx as nx
import random

from sources.graph_view import visualize_graph, analyze_graph
from sources.dijkstra_algorithm import paths_dijkstra
from sources.graph_paths import bfs, dfs
from sources.graph_generator import create_transportation_network


def compare_bfs_dfs():
    # seed for reproducibility
    random.seed(42)

    num_stations = 10
    num_connections = 15

    transportation_network = create_transportation_network(num_stations, num_connections)

    # graph information
    print("=" * 70)
    print("TRANSPORTATION NETWORK ANALYSIS")
    print("=" * 70)
    print(f"\nGraph Statistics:")
    print(f"  - Number of stations (nodes): {transportation_network.number_of_nodes()}")
    print(f"  - Number of connections (edges): {transportation_network.number_of_edges()}")
    print(f"  - Is connected: {nx.is_connected(transportation_network)}")
    print(f"\nEdges in the graph:")
    for edge in transportation_network.edges():
        print(f"  {edge[0]} <-> {edge[1]}")

    print("\n" + "=" * 70)
    print("PATH FINDING COMPARISON: BFS vs DFS")
    print("=" * 70)

    start_station = "Station_1"
    goal_station = "Station_5"

    print(f"\nSearching for path from '{start_station}' to '{goal_station}'...\n")

    bfs_path = bfs(transportation_network, start_station, goal_station)
    dfs_path = dfs(transportation_network, start_station, goal_station)

    if bfs_path:
        print(f"BFS Path: {' -> '.join(bfs_path)}")
        print(f"BFS Path Length: {len(bfs_path)} stations ({len(bfs_path) - 1} connections)")
    else:
        print(f"BFS: No path found from {start_station} to {goal_station}")

    print()

    if dfs_path:
        print(f"DFS Path: {' -> '.join(dfs_path)}")
        print(f"DFS Path Length: {len(dfs_path)} stations ({len(dfs_path) - 1} connections)")
    else:
        print(f"DFS: No path found from {start_station} to {goal_station}")

    print("\n" + "=" * 70)
    print("COMPARISON ANALYSIS")
    print("=" * 70)

    if bfs_path and dfs_path:
        print(f"\nPaths are {'IDENTICAL' if bfs_path == dfs_path else 'DIFFERENT'}")
        if bfs_path != dfs_path:
            print(f"  - BFS path length: {len(bfs_path) - 1} connections")
            print(f"  - DFS path length: {len(dfs_path) - 1} connections")
            print(f"  - Difference: {abs(len(bfs_path) - len(dfs_path))} connections")

    print("\n" + "=" * 70)
    print("\nKEY INSIGHTS:")
    print("""
BFS (Breadth-First Search):
  ✓ Explores all neighbors at the current depth before moving deeper
  ✓ ALWAYS finds the shortest path (minimum number of edges)
  ✓ Uses more memory (stores all nodes at current level)
  ✓ Ideal for finding shortest paths in unweighted graphs

DFS (Depth-First Search):
  ✓ Explores as far as possible along each branch before backtracking
  ✓ May NOT find the shortest path (depends on graph structure)
  ✓ Uses less memory (only stores current path)
  ✓ Ideal for exploring all possible paths or checking connectivity
    """)


if __name__ == "__main__":
    while True:
        print("\n************ MENU ************")
        print("1. Visualize and Analyze Transportation Network")
        print("2. Compare BFS and DFS Path Finding")
        print("3. Dijkstra's Shortest Path Algorithm")
        print("4. Exit")
        print("******************************")

        choice = input("Select an option: ")
        if choice == '1':
            num_stations = 10
            num_connections = 15

            transportation_network = create_transportation_network(num_stations, num_connections)
            analyze_graph(transportation_network)
            visualize_graph(transportation_network)

        elif choice == '2':
            compare_bfs_dfs()

        elif choice == '3':
            num_stations = 10
            num_connections = 15

            transportation_network = create_transportation_network(num_stations, num_connections, weights=True)

            start_station = "Station_1"
            shortest_paths = paths_dijkstra(transportation_network, start_station)

            print(f"\nDijkstra's Shortest Paths from '{start_station}':\n")
            for station, (distance, path) in shortest_paths.items():
                print(f"  To {station}: Distance = {distance}, Path = {' -> '.join(path)}")

        elif choice == '4':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")
