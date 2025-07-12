import heapq

def astar(graph, start, goal, heuristic):
    pq = [(heuristic[start], 0, start, [start])]  # (f(n), g(n), current, path)
    visited = set()
    steps = []

    while pq:
        f, g, current, path = heapq.heappop(pq)
        steps.append((current, list(pq), list(visited), path, g, heuristic[current], f))

        if current == goal:
            return path, g, steps

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                new_g = g + weight
                new_f = new_g + heuristic.get(neighbor, float('inf'))
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    return None, float('inf'), steps
