import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import math, json
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
        self.auto_running = False
        self.timer_id = None

        self.setup_ui()

    def setup_ui(self):
        frame_top = tk.Frame(self.root)
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="یال (از، به، وزن):").grid(row=0, column=0)
        self.edge_from = tk.Entry(frame_top, width=5)
        self.edge_from.grid(row=0, column=1)
        self.edge_to = tk.Entry(frame_top, width=5)
        self.edge_to.grid(row=0, column=2)
        self.edge_weight = tk.Entry(frame_top, width=5)
        self.edge_weight.grid(row=0, column=3)
        tk.Button(frame_top, text="افزودن یال", command=self.add_edge).grid(row=0, column=4)

        frame_middle = tk.Frame(self.root)
        frame_middle.pack(pady=5)

        tk.Label(frame_middle, text="مبدا:").grid(row=0, column=0)
        self.start_entry = tk.Entry(frame_middle, width=5)
        self.start_entry.grid(row=0, column=1)
        tk.Label(frame_middle, text="مقصد:").grid(row=0, column=2)
        self.goal_entry = tk.Entry(frame_middle, width=5)
        self.goal_entry.grid(row=0, column=3)

        self.algorithm_var = tk.StringVar(value="BFS")
        algo_menu = ttk.Combobox(frame_middle, textvariable=self.algorithm_var, values=["BFS", "DFS", "UCS", "A*"])
        algo_menu.grid(row=0, column=4)

        tk.Button(frame_middle, text="شروع", command=self.run_algorithm).grid(row=0, column=5)
        tk.Button(frame_middle, text="مرحله بعد →", command=self.next_step).grid(row=0, column=6)
        tk.Button(frame_middle, text="▶️ اجرا خودکار", command=self.start_auto).grid(row=0, column=7)
        tk.Button(frame_middle, text="⏹ توقف", command=self.stop_auto).grid(row=0, column=8)

        frame_bottom = tk.Frame(self.root)
        frame_bottom.pack(pady=5)

        tk.Button(frame_bottom, text="ریست گراف", command=self.reset_graph).grid(row=0, column=0)
        tk.Button(frame_bottom, text="ذخیره گراف", command=self.save_graph).grid(row=0, column=1)
        tk.Button(frame_bottom, text="بارگذاری گراف", command=self.load_graph).grid(row=0, column=2)
        tk.Button(frame_bottom, text="محاسبه h(n)", command=lambda: self.calculate_heuristic(self.goal_entry.get())).grid(row=0, column=3)

        self.canvas = tk.Canvas(self.root, width=600, height=400, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.canvas_click)
        self.canvas.bind("<Button-3>", self.right_click_node)

        self.text_output = tk.Text(self.root, width=80, height=15)
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
            self.text_output.insert(tk.END, f"گره '{name}' در ({event.x}, {event.y}) افزوده شد\n")

    def right_click_node(self, event):
        node = self.get_node_at(event.x, event.y)
        if node:
            win = tk.Toplevel(self.root)
            win.title("تنظیم h(n)")
            tk.Label(win, text=f"مقدار h({node}):").pack()
            entry = tk.Entry(win)
            entry.pack()
            def confirm():
                try:
                    val = float(entry.get())
                    self.heuristic[node] = val
                    self.text_output.insert(tk.END, f"h({node}) = {val} ثبت شد\n")
                    win.destroy()
                except:
                    messagebox.showerror("خطا", "مقدار نامعتبر است.")
            tk.Button(win, text="ثبت", command=confirm).pack()

    def get_node_at(self, x, y):
        for node in self.graph.get_nodes():
            nx, ny = self.graph.get_position(node)
            if (x - nx)**2 + (y - ny)**2 <= 15**2:
                return node
        return None

    def ask_edge_weight_and_add(self):
        f, t = self.edge_click_nodes
        win = tk.Toplevel(self.root)
        win.title("وزن یال")
        tk.Label(win, text=f"وزن {f} → {t}:").pack()
        entry = tk.Entry(win)
        entry.pack()
        def confirm():
            try:
                w = int(entry.get())
                self.graph.add_edge(f, t, w)
                self.draw_graph()
                self.text_output.insert(tk.END, f"یال ({f} → {t}, وزن={w}) افزوده شد\n")
                win.destroy()
            except:
                messagebox.showerror("خطا", "وزن نامعتبر است.")
        tk.Button(win, text="افزودن", command=confirm).pack()

    def add_edge(self):
        f, t = self.edge_from.get(), self.edge_to.get()
        try:
            w = int(self.edge_weight.get())
        except:
            messagebox.showerror("خطا", "وزن نامعتبر است")
            return
        self.graph.add_edge(f, t, w)
        self.edge_from.delete(0, tk.END)
        self.edge_to.delete(0, tk.END)
        self.edge_weight.delete(0, tk.END)
        self.draw_graph()
        self.text_output.insert(tk.END, f"یال ({f} → {t}, وزن={w}) افزوده شد\n")

    def run_algorithm(self):
        start, goal = self.start_entry.get(), self.goal_entry.get()
        algo = self.algorithm_var.get()
        if start not in self.graph.nodes or goal not in self.graph.nodes:
            messagebox.showerror("خطا", "گره‌ها نامعتبرند")
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
            self.text_output.insert(tk.END, "مسیر یافت نشد.\n")
        else:
            self.next_step()

    def next_step(self):
        if self.current_step >= len(self.steps):
            self.text_output.insert(tk.END, f"\n🎯 مسیر نهایی: {self.final_path}\n💰 هزینه کل: {self.total_cost}\n")
            self.draw_graph(final_path=set(self.final_path))
            return
        step = self.steps[self.current_step]
        algo = self.algorithm_var.get()
        if algo == "A*":
            node, queue, visited, path, g, h, f = step
            open_set = [item[2] for item in queue]
        else:
            node, queue, visited, path, g = step
            open_set = [item[0] for item in queue]

        self.text_output.insert(tk.END, f"{self.current_step+1}) بررسی: {node} | مسیر: {path}")
        if algo == "A*":
            self.text_output.insert(tk.END, f" | g={g}, h={h}, f={f}\n")
        else:
            self.text_output.insert(tk.END, f" | هزینه: {g}\n")
        self.draw_graph({"open": set(open_set), "closed": set(visited), "current": node})
        self.current_step += 1
        if self.auto_running:
            self.timer_id = self.root.after(800, self.next_step)

    def draw_graph(self, highlights=None, final_path=None):
        self.canvas.delete("all")

        # رسم یال‌ها با جلوگیری از تکرار
        drawn_edges = set()
        for node in self.graph.get_nodes():
            x, y = self.graph.get_position(node)
            for neighbor, weight in self.graph.neighbors(node):
                edge_key = tuple(sorted((node, neighbor)))
                if edge_key in drawn_edges:
                    continue
                drawn_edges.add(edge_key)
                x2, y2 = self.graph.get_position(neighbor)
                self.canvas.create_line(x, y, x2, y2, fill="gray", width=2)
                mx, my = (x + x2) // 2, (y + y2) // 2
                self.canvas.create_text(mx, my, text=str(weight), fill="black", font=("Arial", 9))

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
            if final_path and node in final_path: color = "red"
            if node == self.start_entry.get(): color = "yellow"
            if node == self.goal_entry.get(): color = "green"

            self.canvas.create_oval(x - 15, y - 15, x + 15, y + 15, fill=color)
            self.canvas.create_text(x, y, text=node, font=("Arial", 10, "bold"))

            # نمایش مقدار h(n) کنار گره به رنگ خاکستری و فونت کوچکتر
            h_val = self.heuristic.get(node, 0)
            self.canvas.create_text(x + 20, y, text=f"h={h_val}", fill="gray30", font=("Arial", 8, "italic"))

    def save_graph(self):
        data = {
            "nodes": {
                node: {
                    "pos": self.graph.get_position(node),
                    "h": self.heuristic.get(node, 0)
                }
                for node in self.graph.get_nodes()
            },
            "edges": []
        }

        added_edges = set()
        for node in self.graph.get_nodes():
            for neighbor, weight in self.graph.neighbors(node):
                # از ذخیره‌سازی یال‌های تکراری جلوگیری می‌کنیم
                edge_key = tuple(sorted((node, neighbor)))
                if edge_key not in added_edges:
                    data["edges"].append({
                        "from": node,
                        "to": neighbor,
                        "weight": weight
                    })
                    added_edges.add(edge_key)

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)  # ✔ ایندنت مرتب شده
            self.text_output.insert(tk.END, f"✅ گراف با موفقیت ذخیره شد: {file_path}\n")

    def load_graph(self):
        file = filedialog.askopenfilename(filetypes=[("JSON", "*.json")])
        if not file: return
        data = json.load(open(file))
        self.graph = Graph()
        self.heuristic = {}
        for n, v in data["nodes"].items():
            self.graph.add_node(n, tuple(v["pos"]))
            self.heuristic[n] = v.get("h", 0)
        for e in data["edges"]:
            self.graph.add_edge(e["from"], e["to"], e["weight"])
        self.draw_graph()
        self.text_output.insert(tk.END, f"📥 گراف بارگذاری شد: {file}\n")

    def calculate_heuristic(self, goal_node):
        if goal_node not in self.graph.nodes:
            messagebox.showerror("خطا", "گره مقصد معتبر نیست")
            return

        def compute_heuristics(mode):
            gx, gy = self.graph.get_position(goal_node)
            for node in self.graph.get_nodes():
                x, y = self.graph.get_position(node)
                if mode == "اقلیدسی":
                    dist = ((x - gx) ** 2 + (y - gy) ** 2) ** 0.5
                elif mode == "مانهتن":
                    dist = abs(x - gx) + abs(y - gy)
                elif mode == "صفر":
                    dist = 0
                else:
                    dist = 0
                self.heuristic[node] = round(dist, 2)

            self.text_output.insert(tk.END, f"📐 h(n) به صورت '{mode}' محاسبه شد.\n")

        # پنجره انتخاب نوع تابع
        win = tk.Toplevel(self.root)
        win.title("انتخاب تابع هیوریستیک")

        tk.Label(win, text="نوع تابع هیوریستیک:").pack(pady=5)
        mode_var = tk.StringVar(value="اقلیدسی")
        for opt in ["اقلیدسی", "مانهتن", "صفر"]:
            tk.Radiobutton(win, text=opt, variable=mode_var, value=opt).pack(anchor=tk.W)

        tk.Button(win, text="محاسبه", command=lambda: [compute_heuristics(mode_var.get()), win.destroy()]).pack(pady=10)

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
