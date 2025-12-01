from typing import List
import random
import timeit
import sys
sys.setrecursionlimit(10**6)


def merge_sort(arr: List[int]) -> List[int]:
    if len(arr) > 1:
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1
    return arr


def insertion_sort(arr: List[int]) -> List[int]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def generate_random_list(size: int) -> List[int]:
    return [random.randint(0, size) for _ in range(size)]


def measure_time(sort_func, arr: List[int], number: int = 5) -> float:
    timer = timeit.Timer(lambda: sort_func(arr.copy()))
    return timer.timeit(number=number) / number


if __name__ == "__main__":
    sizes = [100, 1000, 5000, 10000]
    for size in sizes:
        arr = generate_random_list(size)

        merge_time = measure_time(merge_sort, arr)
        insertion_time = measure_time(insertion_sort, arr)
        timsort_time = measure_time(sorted, arr)

        print(f"Array Size: {size}")
        print(f"Merge Sort Time: {merge_time:.6f} seconds")
        print(f"Insertion Sort Time: {insertion_time:.6f} seconds")
        print(f"Timsort (built-in sorted) Time: {timsort_time:.6f} seconds")
        print("-" * 40)
