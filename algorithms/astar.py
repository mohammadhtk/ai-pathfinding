import heapq

def astar(graph, start, goal, heuristic):
    # Priority queue stores nodes as tuples: (f(n), g(n), current_node, path_taken)
    # f(n) = g(n) + h(n), where:
    #   g(n) = cost so far
    #   h(n) = heuristic estimate to goal
    pq = [(heuristic[start], 0, start, [start])]
    visited = set()   # Keeps track of explored nodes
    steps = []        # For debugging/visualization: logs each step of the algorithm

    while pq:
        # Pop the node with the lowest f(n) from the priority queue
        f, g, current, path = heapq.heappop(pq)

        # Record the current state for step tracking
        steps.append((
            current,          # Current node
            list(pq),         # Snapshot of priority queue
            list(visited),    # Nodes already visited
            path,             # Path taken to reach current node
            g,                # Cost so far
            heuristic[current], # Heuristic value h(n)
            f                 # Total estimated cost f(n)
        ))

        # Goal check: if current node is the goal, return the result
        if current == goal:
            return path, g, steps

        # Skip if already visited
        if current in visited:
            continue
        visited.add(current)

        # Explore neighbors of the current node
        for neighbor, weight in graph.neighbors(current):
            if neighbor not in visited:
                new_g = g + weight  # New path cost
                # New f(n) = g(n) + h(n), if heuristic missing use infinity
                new_f = new_g + heuristic.get(neighbor, float('inf'))
                # Push neighbor into priority queue with updated path
                heapq.heappush(pq, (new_f, new_g, neighbor, path + [neighbor]))

    # If goal not found, return failure result
    return None, float('inf'), steps
