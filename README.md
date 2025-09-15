# Pathfinding Visualizer

A Python GUI application to visualize pathfinding algorithms on a custom graph using **Tkinter**. Users can create nodes, add edges, set heuristics, and see step-by-step execution of algorithms like **BFS, DFS, UCS, and A\***.

---

## Features

- **Interactive Graph Editor**
  - Add nodes by clicking on the canvas.
  - Add edges manually or by selecting two nodes.
  - Set edge weights and modify them dynamically.
  - Right-click nodes to set heuristic values for A*.

- **Algorithms Supported**
  - **BFS** (Breadth-First Search)
  - **DFS** (Depth-First Search)
  - **UCS** (Uniform Cost Search)
  - **A\*** (A-Star Search with custom heuristics)

- **Step-by-Step Execution**
  - Navigate forward/backward through algorithm steps.
  - Auto-run with adjustable speed.
  - Visual highlight of open set, closed set, and current node.

- **Graph Management**
  - Save and load graphs in JSON format.
  - Reset the graph to start fresh.

- **Heuristic Calculation**
  - Supports Euclidean, Manhattan, or Zero heuristic functions.
  - Automatic visualization of `h(n)` values for A*.

---

## Installation

No external dependencies are required. Python 3 comes with **Tkinter** and **json** libraries by default.

1. Clone this repository:

```bash
git clone <repository_url>
cd ai-pathfinding
````

---

## Usage

1. Run the gui program:

```bash
python gui.py
```

2. Interact with the GUI:

   * Click to add nodes.
   * Use the **Add Edge** form or select nodes to create edges.
   * Set start and goal nodes.
   * Choose an algorithm from the dropdown.
   * Press **Run** to start the visualization.
   * Use **Next →**, **← Previous**, **▶ Auto Run**, and **⏹ Stop** buttons to navigate algorithm steps.
   * Calculate heuristics via **Calculate h(n)** button.

---

## Example Graph

```text
Nodes: A, B, C, D, E
Edges:
- A → B (2)
- A → C (5)
- B → D (4)
- C → D (1)
- D → E (3)
Heuristic for A*: {A: 6, B: 4, C: 2, D: 1, E: 0}
```

---

## File Structure

```
pathfinding-visualizer/
├── algorithms/
│   ├── bfs.py
│   ├── dfs.py
│   ├── ucs.py
│   └── astar.py
├── graph.py
├── gui.py
├── main.py
└── README.md
└── LICENSE
```

* **graph.py**: Handles graph data structure (nodes, edges, positions).
* **algorithms/**: Implements BFS, DFS, UCS, and A\* algorithms.
* **gui.py**: GUI class using Tkinter for visualization and interaction.
* **main.py**: Entry point to run the GUI application.

---

## License

MIT License © 2025

---

## Author

Mohammad Tavakoli


