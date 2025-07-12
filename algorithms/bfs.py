from collections import deque

def bfs(graph, start, goal):
    visited = set()
    queue = deque([(start, [start])])
    cost = 0
    steps = []

    while queue:
        current, path = queue.popleft()
        steps.append((current, list(queue), list(visited), path, cost))

        if current == goal:
            return path, cost, steps

        if current in visited:
            continue

        visited.add(current)

        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                queue.append((neighbor, path + [neighbor]))
                cost += weight  # در BFS، وزن معمولاً نادیده گرفته می‌شود

    return None, float('inf'), steps
