from typing import List


def merge_k_lists(lists: List[List[int]]) -> List[int]:
    lists_len = len(lists)

    if lists_len == 0:
        return []

    if lists_len == 1:
        return lists[0]

    mid = lists_len // 2

    left_merged = merge_k_lists(lists[:mid])
    right_merged = merge_k_lists(lists[mid:])

    return merge_two_lists(left_merged, right_merged)


def merge_two_lists(list1: List[int], list2: List[int]) -> List[int]:
    merged = []
    i = j = 0

    while i < len(list1) and j < len(list2):
        if list1[i] < list2[j]:
            merged.append(list1[i])
            i += 1
        else:
            merged.append(list2[j])
            j += 1

    while i < len(list1):
        merged.append(list1[i])
        i += 1

    while j < len(list2):
        merged.append(list2[j])
        j += 1

    return merged
