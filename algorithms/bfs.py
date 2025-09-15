from collections import deque

def bfs(graph, start, goal):
    visited = set()                        # Keeps track of visited nodes
    queue = deque([(start, [start])])      # Queue holds tuples: (current_node, path_so_far)
    cost = 0                               # Accumulated cost (⚠️ in BFS, edge weights are usually ignored)
    steps = []                             # Logs the state of the algorithm at each step (for visualization/debugging)

    while queue:
        # Dequeue the first element (FIFO behavior)
        current, path = queue.popleft()

        # Record the current state of the algorithm
        steps.append((
            current,        # Current node
            list(queue),    # Snapshot of the queue
            list(visited),  # Snapshot of visited nodes
            path,           # Path so far
            cost            # Current accumulated cost
        ))

        # Goal check: stop if we reached the target node
        if current == goal:
            return path, cost, steps

        # Skip processing if node already visited
        if current in visited:
            continue

        visited.add(current)

        # Traverse neighbors of the current node
        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                # Append neighbor with updated path to the queue
                queue.append((neighbor, path + [neighbor]))
                # ⚠️ BFS usually ignores weights (all edges assumed cost=1)
                # but here you increment cost by weight (might not be intended for classic BFS)
                cost += weight

    # If no path to goal is found
    return None, float('inf'), steps
