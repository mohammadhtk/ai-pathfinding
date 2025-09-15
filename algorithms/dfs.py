def dfs(graph, start, goal):
    # Stack holds tuples: (current_node, path_so_far, accumulated_cost)
    stack = [(start, [start], 0)]
    visited = set()       # Keeps track of already explored nodes
    steps = []            # For debugging/visualization (captures algorithm state at each step)

    while stack:
        # Pop the last element (LIFO behavior → depth-first search)
        current, path, cost = stack.pop()

        # Log current state
        steps.append((
            current,        # Current node
            list(stack),    # Snapshot of the stack
            list(visited),  # Snapshot of visited nodes
            path,           # Path so far
            cost            # Accumulated path cost
        ))

        # Goal check: if we reached the target, return results
        if current == goal:
            return path, cost, steps

        # Skip if already visited
        if current in visited:
            continue

        visited.add(current)

        # Explore neighbors (reversed so order is consistent with recursive DFS)
        for neighbor, weight in reversed(graph.neighbors(current)):
            if neighbor not in visited:
                # Push neighbor onto stack with updated path and cost
                stack.append((neighbor, path + [neighbor], cost + weight))

    # If goal not found, return failure
    return None, float('inf'), steps
