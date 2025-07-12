import heapq

def ucs(graph, start, goal):
    pq = [(0, start, [start])]
    visited = set()
    steps = []

    while pq:
        cost, current, path = heapq.heappop(pq)
        steps.append((current, list(pq), list(visited), path, cost))

        if current == goal:
            return path, cost, steps

        if current in visited:
            continue
        visited.add(current)

        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    return None, float('inf'), steps
