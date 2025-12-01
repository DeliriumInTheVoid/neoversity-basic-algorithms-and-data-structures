from sources.sorting_algorithms import (
            generate_random_list,
            measure_time,
            merge_sort,
            insertion_sort,
        )

from sources.merge_lists import merge_k_lists


def main():
    while True:
        print("\n************ MENU ************")
        print("1. Compare Sorting Algorithms")
        print("2. Merge K Sorted Lists")
        print("0. Exit")
        print("******************************")

        choice = input("Select an option: ")

        if choice == '1':
            size = 1000
            list_size = input(f"Enter size of array to sort (default {size}): ")
            if list_size.isdigit():
                size = int(list_size)
            else:
                print(f"Using default size: {size}")

            arr = generate_random_list(size)

            merge_time = measure_time(merge_sort, arr)
            insertion_time = measure_time(insertion_sort, arr)
            timsort_time = measure_time(sorted, arr)

            print(f"Array Size: {size}")
            print(f"Merge Sort Time: {merge_time:.6f} seconds")
            print(f"Insertion Sort Time: {insertion_time:.6f} seconds")
            print(f"Timsort (built-in sorted) Time: {timsort_time:.6f} seconds")
            print("-" * 40)

        elif choice == '2':
            lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
            print("Merging the following sorted lists:", lists)
            merged_list = merge_k_lists(lists)
            print("Sorted List:", merged_list)
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
