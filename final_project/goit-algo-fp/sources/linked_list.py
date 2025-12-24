from abc import abstractmethod, ABC
from typing import Literal


SortStrategyType = Literal["merge", "insertion", "quick", "bubble"]

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head: Node | None = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = new_node

    def insert_after(self, prev_node: Node, data):
        if prev_node is None:
            print("Попереднього вузла не існує.")
            return
        new_node = Node(data)
        new_node.next = prev_node.next
        prev_node.next = new_node

    def delete_node(self, key: int):
        cur = self.head
        if cur and cur.data == key:
            self.head = cur.next
            cur = None
            return
        prev = None
        while cur and cur.data != key:
            prev = cur
            cur = cur.next
        if cur is None:
            return
        prev.next = cur.next
        cur = None

    def search_element(self, data: int) -> Node | None:
        cur = self.head
        while cur:
            if cur.data == data:
                return cur
            cur = cur.next
        return None

    def print_list(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def reverse_list(self):
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev

    def merge_sorted(self, other: 'LinkedList') -> 'LinkedList':
        merged_list = LinkedList()
        p1 = self.head
        p2 = other.head

        while p1 and p2:
            if p1.data < p2.data:
                merged_list.insert_at_end(p1.data)
                p1 = p1.next
            else:
                merged_list.insert_at_end(p2.data)
                p2 = p2.next

        p_longer_list = p1 if p1 else p2

        while p_longer_list:
            merged_list.insert_at_end(p_longer_list.data)
            p_longer_list = p_longer_list.next

        return merged_list

    def sort_list(self, strategy: SortStrategyType="merge"):
        strategy_map = {
            "merge": MergeSortStrategy(),
            "insertion": InsertionSortStrategy(),
            "quick": QuickSortStrategy(),
            "bubble": BubbleSortStrategy(),
        }
        sort_strategy = strategy_map.get(strategy, MergeSortStrategy())
        sorted_list = sort_strategy.sort(self)
        self.head = sorted_list.head

    # def sort_list(self, strategy: SortStrategy=None):
    #     if strategy is None:
    #         strategy = MergeSortStrategy()
    #     sorted_list = strategy.sort(self)
    #     self.head = sorted_list.head


    def __iter__(self):
        current = self.head
        while current:
            yield current.data
            current = current.next

    def __str__(self):
        return "->".join(str(data) for data in self)


class SortStrategy(ABC):
    @abstractmethod
    def sort(self, linked_list: LinkedList) -> LinkedList:
        raise NotImplementedError("Sort method must be implemented by subclasses.")


class MergeSortStrategy(SortStrategy):
    def sort(self, linked_list: LinkedList) -> LinkedList:
        if linked_list.head is None or linked_list.head.next is None:
            return linked_list

        mid = self.get_middle(linked_list.head)
        next_to_mid = mid.next
        mid.next = None

        left_half = LinkedList()
        left_half.head = linked_list.head
        right_half = LinkedList()
        right_half.head = next_to_mid

        left_sorted = self.sort(left_half)
        right_sorted = self.sort(right_half)

        sorted_list = left_sorted.merge_sorted(right_sorted)
        return sorted_list

    def get_middle(self, node: Node) -> Node:
        if node is None:
            return node

        slow = node
        fast = node.next

        while fast is not None:
            fast = fast.next
            if fast is not None:
                slow = slow.next
                fast = fast.next

        return slow


class InsertionSortStrategy(SortStrategy):
    def sort(self, linked_list: LinkedList) -> LinkedList:
        sorted_list = LinkedList()
        current = linked_list.head

        while current:
            next_node = current.next
            if sorted_list.head is None or sorted_list.head.data >= current.data:
                current.next = sorted_list.head
                sorted_list.head = current
            else:
                sorted_current = sorted_list.head
                while (sorted_current.next is not None and
                       sorted_current.next.data < current.data):
                    sorted_current = sorted_current.next
                current.next = sorted_current.next
                sorted_current.next = current
            current = next_node

        return sorted_list


class QuickSortStrategy(SortStrategy):
    def sort(self, linked_list: LinkedList) -> LinkedList:
        if linked_list.head is None or linked_list.head.next is None:
            return linked_list

        pivot = linked_list.head
        left_list = LinkedList()
        right_list = LinkedList()
        current = pivot.next

        while current:
            if current.data < pivot.data:
                left_list.insert_at_end(current.data)
            else:
                right_list.insert_at_end(current.data)
            current = current.next

        left_sorted = self.sort(left_list)
        right_sorted = self.sort(right_list)

        sorted_list = LinkedList()

        if left_sorted.head:
            sorted_list.head = left_sorted.head
            tail = left_sorted.head
            while tail.next:
                tail = tail.next
            tail.next = pivot
        else:
            sorted_list.head = pivot

        pivot.next = right_sorted.head

        return sorted_list


class BubbleSortStrategy(SortStrategy):
    def sort(self, linked_list: LinkedList) -> LinkedList:
        if linked_list.head is None:
            return linked_list

        swapped = True
        while swapped:
            swapped = False
            current = linked_list.head
            while current and current.next:
                if current.data > current.next.data:
                    current.data, current.next.data = current.next.data, current.data
                    swapped = True
                current = current.next

        return linked_list


def generate_random_linked_list(size: int, value_range: tuple = (0, 100), sorted:bool=False) -> LinkedList:
    import random

    llist = LinkedList()
    for _ in range(size):
        llist.insert_at_end(random.randint(*value_range))
    if sorted:
        llist.sort_list()
    return llist


if __name__ == "__main__":
    llist = LinkedList()

    # Вставляємо вузли в початок
    llist.insert_at_beginning(5)
    llist.insert_at_beginning(10)
    llist.insert_at_beginning(15)

    # Вставляємо вузли в кінець
    llist.insert_at_end(20)
    llist.insert_at_end(25)

    # Друк зв'язного списку
    print("Зв'язний список:")
    llist.print_list()

    # Видаляємо вузол
    llist.delete_node(10)

    print("\nЗв'язний список після видалення вузла з даними 10:")
    llist.print_list()

    # Пошук елемента у зв'язному списку
    print("\nШукаємо елемент 15:")
    element = llist.search_element(15)
    if element:
        print(element.data)
