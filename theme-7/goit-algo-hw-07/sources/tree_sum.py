from .avl_tree import AVLNode


def tree_sum(root: AVLNode | None) -> int:
    if root is None:
        return 0
    return root.key + tree_sum(root.left) + tree_sum(root.right)
