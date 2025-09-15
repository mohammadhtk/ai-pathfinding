import heapq

def ucs(graph, start, goal):
    # Priority queue holds tuples: (cost_so_far, current_node, path_so_far)
    pq = [(0, start, [start])]
    visited = set()   # Keeps track of expanded nodes
    steps = []        # For logging/visualization

    while pq:
        # Pop the node with the smallest cumulative cost
        cost, current, path = heapq.heappop(pq)

        # Log current state
        steps.append((
            current,       # Current node
            list(pq),      # Snapshot of the priority queue
            list(visited), # Snapshot of visited nodes
            path,          # Path so far
            cost           # Cost so far
        ))

        # Goal check: if we reached the target, return result
        if current == goal:
            return path, cost, steps

        # Skip if already visited (prevents re-expansion)
        if current in visited:
            continue
        visited.add(current)

        # Explore neighbors
        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                # Push neighbor into priority queue with updated cumulative cost
                heapq.heappush(pq, (cost + weight, neighbor, path + [neighbor]))

    # If no path to goal found
    return None, float('inf'), steps
