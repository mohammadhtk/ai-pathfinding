class Graph:
    def __init__(self):
        self.nodes = {}  # {name: (x, y)}
        self.edges = {}  # {name: [(neighbor, weight)]}

    def add_node(self, name, pos):
        self.nodes[name] = pos
        if name not in self.edges:
            self.edges[name] = []

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append((to_node, weight))
        self.edges[to_node].append((from_node, weight))  # گراف بدون جهت

    def neighbors(self, node):
        return self.edges.get(node, [])

    def get_nodes(self):
        return list(self.nodes.keys())

    def get_position(self, node):
        return self.nodes.get(node)

