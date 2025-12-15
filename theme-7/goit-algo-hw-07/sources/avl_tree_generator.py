from typing import Tuple

from .avl_tree import AVLNode, insert
from random import randint


def generate_avl_tree(values: int) -> Tuple[AVLNode | None, list[int]]:
    root = None
    unique_values = set()

    while len(unique_values) < values:
        value = randint(1, values * 10)
        if value not in unique_values:
            unique_values.add(value)
            root = insert(root, value)

    return root, list(unique_values)
