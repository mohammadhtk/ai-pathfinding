from graph import Graph
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar

# Create graph
graph = Graph()
positions = {
    "A": (0, 0),
    "B": (1, 0),
    "C": (0, 1),
    "D": (1, 1),
    "E": (2, 1)
}

for node, pos in positions.items():
    graph.add_node(node, pos)

graph.add_edge("A", "B", 2)
graph.add_edge("A", "C", 5)
graph.add_edge("B", "D", 4)
graph.add_edge("C", "D", 1)
graph.add_edge("D", "E", 3)

# Heuristic for A*
heuristic = {
    "A": 6,
    "B": 4,
    "C": 2,
    "D": 1,
    "E": 0
}

# Test DFS
print("\n--- DFS ---")
path, cost, _ = dfs(graph, "A", "E")
print("Path:", path, "| Cost:", cost)

# Test UCS
print("\n--- UCS ---")
path, cost, _ = ucs(graph, "A", "E")
print("Path:", path, "| Cost:", cost)

# Test A*
print("\n--- A* ---")
path, cost, _ = astar(graph, "A", "E", heuristic)
print("Path:", path, "| Cost:", cost)
