from .avl_tree import AVLNode


def find_max_in_tree(root: AVLNode) -> int:
    if root is None:
        raise ValueError("The tree is empty")

    current = root
    while current.right is not None:
        current = current.right

    return current.key
