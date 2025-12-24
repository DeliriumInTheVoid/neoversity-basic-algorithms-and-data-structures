import uuid
import networkx as nx
import matplotlib.pyplot as plt


class Node:
    def __init__(self, value, color="skyblue"):
        self.left = None
        self.right = None
        self.val = value
        self.color = color
        self.id = str(uuid.uuid4())


def add_edges(graph, node, pos, x=0, y=0, layer=1):
    if node is None:
        return graph

    graph.add_node(node.id, color=node.color, label=node.val)

    if node.left:
        graph.add_edge(node.id, node.left.id)
        lx = x - 1 / (2 ** layer)
        pos[node.left.id] = (lx, y - 1)
        add_edges(graph, node.left, pos, x=lx, y=y - 1, layer=layer + 1)

    if node.right:
        graph.add_edge(node.id, node.right.id)
        rx = x + 1 / (2 ** layer)
        pos[node.right.id] = (rx, y - 1)
        add_edges(graph, node.right, pos, x=rx, y=y - 1, layer=layer + 1)

    return graph


def draw_tree(root):
    graph = nx.DiGraph()
    pos = {root.id: (0, 0)}
    add_edges(graph, root, pos)

    colors = [n[1]["color"] for n in graph.nodes(data=True)]
    labels = {n[0]: n[1]["label"] for n in graph.nodes(data=True)}

    plt.figure(figsize=(10, 6))
    nx.draw(graph, pos=pos, labels=labels, arrows=False, node_size=2500, node_color=colors)
    plt.show()


def heapify_in_place(arr, heap_type="min"):
    """
    Bottom-up heapify in O(n).
    heap_type: "min" or "max"
    Note: values must be comparable (e.g., ints, floats).
    """
    if heap_type not in ("min", "max"):
        raise ValueError("heap_type must be 'min' or 'max'")

    def better(a, b):
        return a < b if heap_type == "min" else a > b

    def sift_down(i, n):
        while True:
            left = 2 * i + 1
            right = 2 * i + 2
            best = i

            if left < n and better(arr[left], arr[best]):
                best = left
            if right < n and better(arr[right], arr[best]):
                best = right

            if best == i:
                break

            arr[i], arr[best] = arr[best], arr[i]
            i = best

    n = len(arr)
    for i in range(n // 2 - 1, -1, -1):
        sift_down(i, n)

    return arr


def heap_array_to_tree(heap_array, root_color="gold"):
    if not heap_array:
        return None

    nodes = [Node(v) for v in heap_array]

    for i in range(len(nodes)):
        li = 2 * i + 1
        ri = 2 * i + 2

        if li < len(nodes):
            nodes[i].left = nodes[li]
        if ri < len(nodes):
            nodes[i].right = nodes[ri]

    nodes[0].color = root_color
    return nodes[0]


def validate_heap_colors(heap_array, heap_type="min"):
    """
    Colors children that violate the heap property relative to their parent.
    Returns a list of colors aligned with heap_array indices.
    """
    if heap_type not in ("min", "max"):
        raise ValueError("heap_type must be 'min' or 'max'")

    colors = ["skyblue"] * len(heap_array)

    def violates(parent, child):
        return parent > child if heap_type == "min" else parent < child

    for i in range(len(heap_array)):
        li = 2 * i + 1
        ri = 2 * i + 2
        if li < len(heap_array) and violates(heap_array[i], heap_array[li]):
            colors[li] = "tomato"
        if ri < len(heap_array) and violates(heap_array[i], heap_array[ri]):
            colors[ri] = "tomato"

    colors[0] = "gold"
    return colors


def draw_heap(data, heap_type="min", heapify=True, validate=False):
    """
    data: input array (any order) OR already-heapified array (if heapify=False)
    heap_type: "min" or "max"
    heapify: if True, builds a heap from data first
    validate: if True, highlights violations (useful when heapify=False)
    """
    heap_array = list(data)

    if heapify:
        heapify_in_place(heap_array, heap_type=heap_type)

    root = heap_array_to_tree(heap_array)
    if root is None:
        print("Empty heap: nothing to draw.")
        return

    if validate:
        colors = validate_heap_colors(heap_array, heap_type=heap_type)
        nodes = [Node(v, color=colors[i]) for i, v in enumerate(heap_array)]
        for i in range(len(nodes)):
            li = 2 * i + 1
            ri = 2 * i + 2
            if li < len(nodes):
                nodes[i].left = nodes[li]
            if ri < len(nodes):
                nodes[i].right = nodes[ri]
        root = nodes[0]

    draw_tree(root)


if __name__ == "__main__":
    # Example: build a MIN-heap from an arbitrary array, then draw it
    data = [4, 10, 3, 5, 1, 0, 8]
    draw_heap(data, heap_type="min", heapify=True, validate=False)

    # Example: build a MAX-heap from an arbitrary array, then draw it
    data2 = [4, 10, 3, 5, 1, 0, 8]
    draw_heap(data2, heap_type="max", heapify=True, validate=False)

    # Example: visualize an already-heap array and highlight violations (if any)
    maybe_heap = [0, 1, 3, 4, 5, 10, 8]
    draw_heap(maybe_heap, heap_type="min", heapify=False, validate=True)
