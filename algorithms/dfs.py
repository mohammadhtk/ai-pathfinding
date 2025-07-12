def dfs(graph, start, goal):
    stack = [(start, [start], 0)]
    visited = set()
    steps = []

    while stack:
        current, path, cost = stack.pop()
        steps.append((current, list(stack), list(visited), path, cost))

        if current == goal:
            return path, cost, steps

        if current in visited:
            continue

        visited.add(current)

        for neighbor, weight in reversed(graph.neighbors(current)):
            if neighbor not in visited:
                stack.append((neighbor, path + [neighbor], cost + weight))

    return None, float('inf'), steps
