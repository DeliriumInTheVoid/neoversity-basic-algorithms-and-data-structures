from .pyramid_visualizer import Node, heap_array_to_tree, heapify_in_place
from collections import deque
import turtle


# -------------------------
# from binary tree node (task 4)
# -------------------------
# class Node:
#     def __init__(self, value, color="skyblue"):
#         self.left = None
#         self.right = None
#         self.val = value
#         self.color = color
#         self.id = str(uuid.uuid4())


# -------------------------
# color gradient (HEX)
# -------------------------
def hex_to_rgb(hex_color: str) -> tuple[int, int, int]:
    h = hex_color.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    r, g, b = rgb
    return f"#{r:02X}{g:02X}{b:02X}"


def make_gradient_colors(n: int, start_hex="#0B1F3A", end_hex="#BFE8FF") -> list[str]:
    if n <= 0:
        return []
    if n == 1:
        return [end_hex.upper()]

    sr, sg, sb = hex_to_rgb(start_hex)
    er, eg, eb = hex_to_rgb(end_hex)

    colors = []
    for i in range(n):
        t = i / (n - 1)
        r = int(sr + (er - sr) * t)
        g = int(sg + (eg - sg) * t)
        b = int(sb + (eb - sb) * t)
        colors.append(rgb_to_hex((r, g, b)))
    return colors


def collect_nodes_iterative(root: Node) -> list[Node]:
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        if node.right is not None:
            stack.append(node.right)
        if node.left is not None:
            stack.append(node.left)
    return nodes


def compute_layout(root: Node) -> dict[str, tuple[float, float]]:
    pos = {root.id: (0.0, 0.0)}
    stack = [(root, 0.0, 0.0, 1)]  # (node, x, y, layer)

    while stack:
        node, x, y, layer = stack.pop()
        pos[node.id] = (x, y)

        if node.left is not None:
            lx = x - 1.0 / (2 ** layer)
            pos[node.left.id] = (lx, y - 1.0)
            stack.append((node.left, lx, y - 1.0, layer + 1))

        if node.right is not None:
            rx = x + 1.0 / (2 ** layer)
            pos[node.right.id] = (rx, y - 1.0)
            stack.append((node.right, rx, y - 1.0, layer + 1))

    return pos


def scale_layout_to_screen(pos_norm: dict[str, tuple[float, float]], screen: turtle.Screen) -> dict[str, tuple[float, float]]:
    xs = [p[0] for p in pos_norm.values()]
    ys = [p[1] for p in pos_norm.values()]
    min_x, max_x = min(xs), max(xs)
    min_y = min(ys)  # typically negative
    width = screen.window_width()
    height = screen.window_height()

    panel_width = 320
    usable_width = width - panel_width

    x_span = max(abs(min_x), abs(max_x))
    x_span = x_span if x_span != 0 else 1.0
    x_scale = (usable_width * 0.42) / x_span

    depth = int(round(-min_y))
    level_step = min(90.0, (height - 140.0) / max(1, depth + 1))
    top_y = (height / 2.0) - 70.0

    pos_screen = {}
    for node_id, (x, y) in pos_norm.items():
        pos_screen[node_id] = (x * x_scale - panel_width / 2.0, top_y + y * level_step)
    return pos_screen


NODE_RADIUS = 18


class NodePainter:
    def __init__(self):
        t = turtle.Turtle(visible=False)
        t.speed(0)
        t.penup()
        self.t = t

    def draw(self, x: float, y: float, value, fill_color: str, outline: str = "black"):
        self.t.clear()
        self.t.goto(x, y - NODE_RADIUS)
        self.t.pendown()
        self.t.color(outline, fill_color)
        self.t.begin_fill()
        self.t.circle(NODE_RADIUS)
        self.t.end_fill()
        self.t.penup()

        self.t.goto(x, y - 7)
        self.t.color("black")
        self.t.write(str(value), align="center", font=("Arial", 12, "bold"))


def draw_edges_once(root: Node, pos: dict[str, tuple[float, float]]):
    edge_t = turtle.Turtle(visible=False)
    edge_t.speed(0)
    edge_t.pensize(2)
    edge_t.color("#333333")
    edge_t.penup()

    stack = [root]
    while stack:
        node = stack.pop()
        x1, y1 = pos[node.id]

        if node.left is not None:
            x2, y2 = pos[node.left.id]
            edge_t.goto(x1, y1)
            edge_t.pendown()
            edge_t.goto(x2, y2)
            edge_t.penup()
            stack.append(node.left)

        if node.right is not None:
            x2, y2 = pos[node.right.id]
            edge_t.goto(x1, y1)
            edge_t.pendown()
            edge_t.goto(x2, y2)
            edge_t.penup()
            stack.append(node.right)


class TreeTraversalVisualizer:
    def __init__(self, root: Node):
        self.root = root
        self.nodes = collect_nodes_iterative(root)
        self.node_count = len(self.nodes)

        self.screen = turtle.Screen()
        self.screen.title("Tree Traversal Visualizer (DFS/BFS + Frontier Panel)")
        self.screen.setup(width=1200, height=720)
        self.screen.tracer(0, 0)

        pos_norm = compute_layout(root)
        self.pos = scale_layout_to_screen(pos_norm, self.screen)

        self.node_painters = {node.id: NodePainter() for node in self.nodes}

        # static edges
        draw_edges_once(root, self.pos)

        # panel writer
        self.panel_t = turtle.Turtle(visible=False)
        self.panel_t.speed(0)
        self.panel_t.penup()
        self.panel_t.color("#111111")

        # control state
        self._run_id = 0
        self.delay_ms = 650
        self.colors = make_gradient_colors(self.node_count, start_hex="#0B1F3A", end_hex="#BFE8FF")

        self.mode = None  # "DFS" or "BFS"
        self.frontier_stack = None
        self.frontier_queue = None
        self.visited_index = 0

        # controls
        self.screen.listen()
        self.screen.onkey(self.start_dfs, "d")
        self.screen.onkey(self.start_dfs, "D")
        self.screen.onkey(self.start_bfs, "b")
        self.screen.onkey(self.start_bfs, "B")
        self.screen.onkey(self.reset, "r")
        self.screen.onkey(self.reset, "R")
        self.screen.onkey(self.quit, "q")
        self.screen.onkey(self.quit, "Q")

        self.reset()
        self._draw_help()

    def _draw_help(self):
        help_t = turtle.Turtle(visible=False)
        help_t.speed(0)
        help_t.penup()
        help_t.color("#111111")
        w = self.screen.window_width()
        h = self.screen.window_height()
        help_t.goto(-w / 2 + 20, h / 2 - 40)
        help_t.write("D: DFS (stack)   B: BFS (queue)   R: Reset   Q: Quit",
                     font=("Arial", 12, "normal")) # size 12 = 19px height

    def _panel_anchor(self, num_text_lines: int) -> tuple[float, float]:
        w = self.screen.window_width()
        h = self.screen.window_height()
        # x = w / 2 - 300
        # y = h / 2 - 80
        x = w / 2 - 320

        line_height = 19 # approx for font size 12
        total_lines = num_text_lines
        content_height = total_lines * line_height

        top_margin = 50
        y = h / 2 - top_margin - 10 - content_height

        if y - content_height < -h / 2 + 20:
            y = -h / 2 + 20 + content_height

        return x, y

    def _render_panel(self, title: str, lines: list[str], step_info: str):
        self.panel_t.clear()
        lines_count = len(lines)
        if lines_count == 0:
            lines_count += 1
        lines_count += 3  # title + step_info + blank + lines
        x, y = self._panel_anchor(lines_count)
        self.panel_t.goto(x, y)
        text = title + "\n" + step_info + "\n\n" +  "\n".join(lines)
        self.panel_t.write(text, align="left", font=("Consolas", 12, "normal"))
        # self.panel_t.write(text, align="right", font=("Consolas", 12, "normal"))

    def _render_frontier(self, current_node_val=None):
        if self.mode == "DFS":
            frontier = self.frontier_stack[:]  # top is end of list
            # show top first
            display_vals = [str(n.val) for n in reversed(frontier)]
            title = "Frontier: DFS Stack (top → bottom)"
        elif self.mode == "BFS":
            frontier = list(self.frontier_queue)  # front is left of deque
            display_vals = [str(n.val) for n in frontier]
            title = "Frontier: BFS Queue (front → back)"
        else:
            title = "Frontier"
            display_vals = []

        max_lines = 16
        trimmed = display_vals[:max_lines]
        if len(display_vals) > max_lines:
            trimmed.append("...")

        lines = [f"{i+1:>2}. {v}" for i, v in enumerate(trimmed)]
        step_info = f"Visited: {self.visited_index}/{self.node_count}"
        if current_node_val is not None:
            step_info += f" | Current: {current_node_val}"

        self._render_panel(title, lines, step_info)

    def _draw_all_nodes(self):
        for node in self.nodes:
            x, y = self.pos[node.id]
            self.node_painters[node.id].draw(x, y, node.val, node.color)

    def reset(self):
        self._run_id += 1
        self.mode = None
        self.frontier_stack = None
        self.frontier_queue = None
        self.visited_index = 0

        for node in self.nodes:
            node.color = "#D3D3D3"

        self._draw_all_nodes()
        self._render_panel("Frontier", ["(press D or B to start)"], "Visited: 0/{}".format(self.node_count))
        self.screen.title("Tree Traversal Visualizer (DFS/BFS + Frontier Panel)")
        self.screen.update()

    def quit(self):
        self._run_id += 1
        self.screen.bye()

    def start_dfs(self):
        self._run_id += 1
        run_id = self._run_id

        # reset colors
        for node in self.nodes:
            node.color = "#D3D3D3"
        self._draw_all_nodes()

        self.mode = "DFS"
        self.frontier_stack = [self.root]
        self.frontier_queue = None
        self.visited_index = 0

        self._render_frontier()
        self.screen.title("DFS (stack) traversal")
        self.screen.update()

        def step():
            if run_id != self._run_id:
                return
            if not self.frontier_stack:
                self._render_frontier(current_node_val="done")
                self.screen.update()
                return

            node = self.frontier_stack.pop()

            # visit: color by order
            color = self.colors[self.visited_index]
            self.visited_index += 1
            node.color = color
            x, y = self.pos[node.id]
            self.node_painters[node.id].draw(x, y, node.val, node.color)

            # push children: right first, then left (preorder)
            if node.right is not None:
                self.frontier_stack.append(node.right)
            if node.left is not None:
                self.frontier_stack.append(node.left)

            self._render_frontier(current_node_val=node.val)
            self.screen.title(f"DFS (stack) | step {self.visited_index}/{self.node_count} | visit: {node.val}")
            self.screen.update()

            self.screen.ontimer(step, self.delay_ms)

        step()

    def start_bfs(self):
        self._run_id += 1
        run_id = self._run_id

        # reset colors
        for node in self.nodes:
            node.color = "#D3D3D3"
        self._draw_all_nodes()

        self.mode = "BFS"
        self.frontier_queue = deque([self.root])
        self.frontier_stack = None
        self.visited_index = 0

        self._render_frontier()
        self.screen.title("BFS (queue) traversal")
        self.screen.update()

        def step():
            if run_id != self._run_id:
                return
            if not self.frontier_queue:
                self._render_frontier(current_node_val="done")
                self.screen.update()
                return

            node = self.frontier_queue.popleft()

            # visit: color by order
            color = self.colors[self.visited_index]
            self.visited_index += 1
            node.color = color
            x, y = self.pos[node.id]
            self.node_painters[node.id].draw(x, y, node.val, node.color)

            # enqueue children: left then right
            if node.left is not None:
                self.frontier_queue.append(node.left)
            if node.right is not None:
                self.frontier_queue.append(node.right)

            self._render_frontier(current_node_val=node.val)
            self.screen.title(f"BFS (queue) | step {self.visited_index}/{self.node_count} | visit: {node.val}")
            self.screen.update()

            self.screen.ontimer(step, self.delay_ms)

        step()

    def run(self):
        try:
            print("\nVisualization in progress. Click on the window to close it when complete.")
            self.screen.mainloop()
        except turtle.Terminator:
            pass
        finally:
            try:
                turtle.bye()
            except:
                pass


def show_tree_traversal_visualizer(elements_num: int = 25, range_min: int = 1, range_max: int = 100):
    import random

    data = list(random.sample(range(range_min, range_max), elements_num))
    heapify_in_place(data, heap_type="min")
    root = heap_array_to_tree(data)

    TreeTraversalVisualizer(root).run()


if __name__ == "__main__":
    show_tree_traversal_visualizer(elements_num=25, range_min=1, range_max=100)
