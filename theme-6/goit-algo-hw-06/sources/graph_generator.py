import networkx as nx
import random


def create_transportation_network(num_stations: int, num_connections: int, weights: bool = False) -> nx.Graph:
    graph = nx.Graph()

    for i in range(num_stations):
        graph.add_node(f"Station_{i+1}")

    while graph.number_of_edges() < num_connections:
        station_a = f"Station_{random.randint(1, num_stations)}"
        station_b = f"Station_{random.randint(1, num_stations)}"
        if station_a != station_b:
            graph.add_edge(station_a, station_b, weight=random.randint(1, 10) if weights else 1)

    return graph
