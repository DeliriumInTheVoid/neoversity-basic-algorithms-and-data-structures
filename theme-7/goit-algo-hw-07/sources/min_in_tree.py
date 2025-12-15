from .avl_tree import AVLNode


def find_min_in_tree(root: AVLNode) -> int:
    if root is None:
        raise ValueError("The tree is empty")

    current = root
    while current.left is not None:
        current = current.left

    return current.key