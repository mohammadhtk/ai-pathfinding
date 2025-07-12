from graph import Graph
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar

graph = Graph()
for node in ["A", "B", "C", "D", "E"]:
    graph.add_node(node)

graph.add_edge("A", "B", 2)
graph.add_edge("A", "C", 5)
graph.add_edge("B", "D", 4)
graph.add_edge("C", "D", 1)
graph.add_edge("D", "E", 3)

heuristic = {
    "A": 6,
    "B": 4,
    "C": 2,
    "D": 1,
    "E": 0
}

print("\n--- DFS ---")
path, cost, steps = dfs(graph, "A", "E")
print("Path:", path, "| Cost:", cost)

print("\n--- UCS ---")
path, cost, steps = ucs(graph, "A", "E")
print("Path:", path, "| Cost:", cost)

print("\n--- A* ---")
path, cost, steps = astar(graph, "A", "E", heuristic)
print("Path:", path, "| Cost:", cost)
