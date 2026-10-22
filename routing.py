import networkx as nx

def create_network():
    G = nx.Graph()

    connections = [
        ("A", "B", 2),
        ("A", "C", 4),
        ("B", "C", 1),
        ("B", "D", 5),
        ("C", "D", 2),
        ("C", "E", 3),
        ("D", "F", 2),
        ("E", "F", 2),
        ("B", "E", 6)
    ]

    for u, v, cost in connections:
        G.add_edge(u, v, weight=cost)

    return G


def find_route(G, source, destination):
    try:
        path = nx.dijkstra_path(
            G, source, destination, weight="weight"
        )
        cost = nx.dijkstra_path_length(
            G, source, destination, weight="weight"
        )
        return path, cost
    except nx.NetworkXNoPath:
        return None, None