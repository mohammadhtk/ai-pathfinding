class Graph:
    def __init__(self, directed=False):
        # Dictionary to store node positions (useful for visualization)
        # Example: {"A": (x, y), "B": (x, y)}
        self.nodes = {}

        # Dictionary to store adjacency list with weights
        # Example: {"A": [("B", 3), ("C", 5)], "B": [("A", 3)]}
        self.edges = {}

        # Currently unused — graph is always undirected in this implementation
        self.directed = directed

    def add_node(self, name, pos):
        """
        Add a new node to the graph.
        :param name: Node identifier (e.g., "A")
        :param pos: Position (x, y) for visualization
        """
        self.nodes[name] = pos
        if name not in self.edges:
            self.edges[name] = []  # Initialize adjacency list for this node

    def add_edge(self, from_node, to_node, weight):
        """
        Add an edge between two nodes.
        :param from_node: Start node
        :param to_node: End node
        :param weight: Edge weight (cost/distance)
        """
        self.edges[from_node].append((to_node, weight))

        # Always adds reverse edge → graph is undirected
        # ⚠️ Even if directed=True is passed in __init__, this still makes it undirected
        self.edges[to_node].append((from_node, weight))

    def neighbors(self, node):
        """
        Return neighbors of a given node with weights.
        :param node: Node name
        :return: List of tuples [(neighbor, weight), ...]
        """
        return self.edges.get(node, [])

    def get_nodes(self):
        """
        Return a list of all nodes in the graph.
        """
        return list(self.nodes.keys())

    def get_position(self, node):
        """
        Return the (x, y) position of a given node.
        Useful for visualization.
        """
        return self.nodes.get(node)
