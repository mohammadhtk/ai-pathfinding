import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import json
from graph import Graph
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.ucs import ucs
from algorithms.astar import astar

class PathfindingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Visualizer")

        self.graph = Graph()
        self.heuristic = {}
        self.edge_click_nodes = []
        self.node_counter = 1
        self.steps = []
        self.current_step = 0
        self.final_path = []
        self.total_cost = 0
        self.auto_running = False
        self.timer_id = None

        self.setup_ui()

    def setup_ui(self):
        style = ttk.Style()
        style.theme_use("clam")

        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=8)

        tk.Label(frame_top, text="Edge:").grid(row=0, column=0, padx=(0, 5))

        tk.Label(frame_top, text="From:").grid(row=0, column=1)
        self.edge_from = tk.Entry(frame_top, width=5)
        self.edge_from.grid(row=0, column=2, padx=(0, 10))

        tk.Label(frame_top, text="To:").grid(row=0, column=3)
        self.edge_to = tk.Entry(frame_top, width=5)
        self.edge_to.grid(row=0, column=4, padx=(0, 10))

        tk.Label(frame_top, text="Weight:").grid(row=0, column=5)
        self.edge_weight = tk.Entry(frame_top, width=5)
        self.edge_weight.grid(row=0, column=6, padx=(0, 10))

        ttk.Button(frame_top, text="Add Edge", style="Modern.TButton", command=self.add_edge).grid(row=0, column=7,
                                                                                                   padx=(0, 10))

        frame_middle = tk.Frame(self.root)
        frame_middle.pack(pady=5)

        tk.Label(frame_middle, text="Start:").grid(row=0, column=0, )
        self.start_entry = tk.Entry(frame_middle, width=5, )
        self.start_entry.grid(row=0, column=1, padx=(0, 10))

        tk.Label(frame_middle, text="Goal:").grid(row=0, column=2)
        self.goal_entry = tk.Entry(frame_middle, width=5)
        self.goal_entry.grid(row=0, column=3, padx=10)

        self.algorithm_var = tk.StringVar(value="BFS")
        algo_menu = ttk.Combobox(frame_middle, textvariable=self.algorithm_var, values=["BFS", "DFS", "UCS", "A*"], state="readonly")
        algo_menu.grid(row=0, column=4)

        frame_controls = tk.Frame(self.root)
        frame_controls.pack(pady=10)

        tk.Button(frame_controls, text="Run", width=10, command=self.run_algorithm).grid(row=0, column=0, padx=5)
        tk.Button(frame_controls, text="← Previous", width=10, command=self.prev_step).grid(row=0, column=1, padx=5)
        tk.Button(frame_controls, text="Next →", width=10, command=self.next_step).grid(row=0, column=2, padx=5)
        tk.Button(frame_controls, text="▶ Auto Run", width=10, command=self.start_auto).grid(row=0, column=3, padx=5)
        tk.Button(frame_controls, text="⏹ Stop", width=10, command=self.stop_auto).grid(row=0, column=4, padx=5)


        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=5)

        tk.Button(frame_bottom, text="Reset Graph", command=self.reset_graph).grid(row=0, column=0, padx=5)
        tk.Button(frame_bottom, text="Save Graph", command=self.save_graph).grid(row=0, column=1, padx=5)
        tk.Button(frame_bottom, text="Load Graph", command=self.load_graph).grid(row=0, column=2, padx=5)
        tk.Button(frame_bottom, text="Calculate h(n)", command=lambda: self.calculate_heuristic(self.goal_entry.get())).grid(row=0, column=3,
                                                                                                                             padx=5)

        self.canvas = tk.Canvas(self.root, width=700, height=450, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Button-3>", self.right_click_node)

        self.text_output = tk.Text(self.root, width=100, height=15, font=("Consolas", 10))
        self.text_output.pack(pady=10)

    def canvas_click(self, event):
        clicked = self.get_node_at(event.x, event.y)
        if clicked:
            self.edge_click_nodes.append(clicked)
            if len(self.edge_click_nodes) == 2:
                self.ask_edge_weight_and_add()
                self.edge_click_nodes = []
        else:
            name = f"N{self.node_counter}"
            self.node_counter += 1
            self.graph.add_node(name, (event.x, event.y))
            self.heuristic[name] = 0
            self.draw_graph()
            self.text_output.insert(tk.END, f"Node '{name}' added at ({event.x}, {event.y})\n")

    def right_click_node(self, event):
        node = self.get_node_at(event.x, event.y)
        if node:
            win = tk.Toplevel(self.root)
            win.title(f"Set h({node})")
            tk.Label(win, text=f"h({node}):").pack(pady=5)
            entry = tk.Entry(win)
            entry.pack()
            def confirm():
                try:
                    val = float(entry.get())
                    self.heuristic[node] = val
                    self.text_output.insert(tk.END, f"h({node}) = {val}\n")
                    win.destroy()
                    self.draw_graph()
                except:
                    messagebox.showerror("Error", "Invalid value")
            tk.Button(win, text="OK", command=confirm).pack(pady=5)

    def get_node_at(self, x, y):
        for node in self.graph.get_nodes():
            nx, ny = self.graph.get_position(node)
            if (x - nx)**2 + (y - ny)**2 <= 15**2:
                return node
        return None

    def ask_edge_weight_and_add(self):
        f, t = self.edge_click_nodes
        win = tk.Toplevel(self.root)
        win.title("Edge Weight")
        tk.Label(win, text=f"Weight {f} → {t}:").pack()
        entry = tk.Entry(win)
        entry.pack()
        def confirm():
            try:
                w = int(entry.get())
                self.graph.add_edge(f, t, w)
                self.draw_graph()
                self.text_output.insert(tk.END, f"Edge ({f} → {t}, w={w}) added\n")
                win.destroy()
            except:
                messagebox.showerror("Error", "Invalid weight")
        tk.Button(win, text="Add", command=confirm).pack()

    def add_edge(self):
        f, t = self.edge_from.get(), self.edge_to.get()
        try:
            w = int(self.edge_weight.get())
        except:
            messagebox.showerror("Error", "Invalid weight")
            return
        self.graph.add_edge(f, t, w)
        self.edge_from.delete(0, tk.END)
        self.edge_to.delete(0, tk.END)
        self.edge_weight.delete(0, tk.END)
        self.draw_graph()
        self.text_output.insert(tk.END, f"Edge ({f} → {t}, w={w}) added\n")

    def run_algorithm(self):
        start, goal = self.start_entry.get(), self.goal_entry.get()
        algo = self.algorithm_var.get()
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            messagebox.showerror("Error", "Invalid nodes")
            return
        self.text_output.delete("1.0", tk.END)
        self.steps = []
        self.current_step = 0

        if algo == "BFS":
            path, cost, self.steps = bfs(self.graph, start, goal)
        elif algo == "DFS":
            path, cost, self.steps = dfs(self.graph, start, goal)
        elif algo == "UCS":
            path, cost, self.steps = ucs(self.graph, start, goal)
        elif algo == "A*":
            path, cost, self.steps = astar(self.graph, start, goal, self.heuristic)

        self.final_path = path
        self.total_cost = cost
        if not self.steps:
            self.text_output.insert(tk.END, "No path found.\n")
        else:
            self.next_step()

    def next_step(self):
        if self.current_step >= len(self.steps):
            self.text_output.insert(tk.END, f"\n🎯 Final Path: {self.final_path}\n💰 Total Cost: {self.total_cost}\n")
            self.draw_graph(final_path=self.final_path)
            return
        step = self.steps[self.current_step]
        algo = self.algorithm_var.get()
        if algo == "A*":
            node, queue, visited, path, g, h, f = step
            open_set = [item[2] for item in queue]
        else:
            node, queue, visited, path, g = step
            open_set = [item[0] for item in queue]

        self.text_output.insert(tk.END, f"{self.current_step+1}) Node: {node} | Path: {path}")
        if algo == "A*":
            self.text_output.insert(tk.END, f" | g={g}, h={h}, f={f}\n")
        else:
            self.text_output.insert(tk.END, f" | Cost: {g}\n")

        self.draw_graph({"open": set(open_set), "closed": set(visited), "current": node})
        self.current_step += 1
        if self.auto_running:
            self.timer_id = self.root.after(800, self.next_step)

    def prev_step(self):
        if self.current_step <= 1:
            return
        self.current_step -= 2
        self.next_step()

    def draw_graph(self, highlights=None, final_path=None):
        self.canvas.delete("all")

        final_edges = set()
        if final_path and len(final_path) >= 2:
            for i in range(len(final_path) - 1):
                a, b = final_path[i], final_path[i + 1]
                final_edges.add(tuple(sorted((a, b))))

        drawn_edges = set()
        for node in self.graph.get_nodes():
            x, y = self.graph.get_position(node)
            for neighbor, weight in self.graph.neighbors(node):
                edge_key = tuple(sorted((node, neighbor)))
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)

                x2, y2 = self.graph.get_position(neighbor)

                is_final = edge_key in final_edges
                color = "red" if is_final else "gray"
                width = 3 if is_final else 2

                self.canvas.create_line(x, y, x2, y2, fill=color, width=width)

                mx, my = (x + x2) // 2, (y + y2) // 2
                dx, dy = x2 - x, y2 - y
                length = max((dx ** 2 + dy ** 2) ** 0.5, 1)
                offset_x = -dy / length * 10
                offset_y = dx / length * 10
                self.canvas.create_text(mx + offset_x, my + offset_y, text=str(weight), font=("Arial", 9))

        for node in self.graph.get_nodes():
            x, y = self.graph.get_position(node)
            color = "lightblue"
            if highlights:
                if node == highlights.get("current"):
                    color = "orange"
                elif node in highlights.get("open", []):
                    color = "blue"
                elif node in highlights.get("closed", []):
                    color = "gray"
            if final_path and node in final_path:
                color = "red"
            if node == self.start_entry.get():
                color = "yellow"
            if node == self.goal_entry.get():
                color = "green"

            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)
            self.canvas.create_text(x, y, text=node, font=("Arial", 10, "bold"))

            # نمایش h(n)
            h_val = self.heuristic.get(node, 0)
            self.canvas.create_text(x, y + 20, text=f"h={h_val}", font=("Arial", 8), fill="gray")

    def calculate_heuristic(self, goal_node):
        if goal_node not in self.graph.nodes:
            messagebox.showerror("Error", "Invalid goal node")
            return

        def compute(mode):
            gx, gy = self.graph.get_position(goal_node)
            for node in self.graph.get_nodes():
                x, y = self.graph.get_position(node)
                if mode == "Euclidean":
                    h = ((x - gx)**2 + (y - gy)**2)**0.5
                elif mode == "Manhattan":
                    h = abs(x - gx) + abs(y - gy)
                elif mode == "Zero":
                    h = 0
                self.heuristic[node] = round(h, 2)
            self.draw_graph()
            self.text_output.insert(tk.END, f"Heuristic calculated using '{mode}'\n")

        win = tk.Toplevel(self.root)
        win.title("Choose Heuristic")
        tk.Label(win, text="Select Heuristic Function:").pack(pady=5)
        mode_var = tk.StringVar(value="Euclidean")
        for opt in ["Euclidean", "Manhattan", "Zero"]:
            tk.Radiobutton(win, text=opt, variable=mode_var, value=opt).pack(anchor=tk.W)
        tk.Button(win, text="Calculate", command=lambda: [compute(mode_var.get()), win.destroy()]).pack(pady=10)

    def save_graph(self):
        data = {
            "nodes": {n: {"pos": self.graph.get_position(n), "h": self.heuristic.get(n, 0)} for n in self.graph.get_nodes()},
            "edges": []
        }
        seen = set()
        for node in self.graph.get_nodes():
            for neighbor, weight in self.graph.neighbors(node):
                edge = tuple(sorted((node, neighbor)))
                if edge in seen: continue
                seen.add(edge)
                data["edges"].append({"from": node, "to": neighbor, "weight": weight})

        file = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if file:
            with open(file, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.text_output.insert(tk.END, f"Graph saved to: {file}\n")

    def load_graph(self):
        file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not file: return
        with open(file, "r", encoding="utf-8") as f:
            data = json.load(f)
        self.graph = Graph()
        self.heuristic = {}
        for n, v in data["nodes"].items():
            self.graph.add_node(n, tuple(v["pos"]))
            self.heuristic[n] = v.get("h", 0)
        for e in data["edges"]:
            self.graph.add_edge(e["from"], e["to"], e["weight"])
        self.draw_graph()
        self.text_output.insert(tk.END, f"Graph loaded from: {file}\n")

    def reset_graph(self):
        self.graph = Graph()
        self.heuristic = {}
        self.steps = []
        self.edge_click_nodes = []
        self.node_counter = 1
        self.current_step = 0
        self.auto_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
        self.canvas.delete("all")
        self.text_output.delete("1.0", tk.END)

    def start_auto(self):
        self.auto_running = True
        self.next_step()

    def stop_auto(self):
        self.auto_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingGUI(root)
    root.mainloop()
