from random import randint
from sources.cables_sort import minimize_cable_cost
from sources.lists_merge import merge_k_lists


def main():
    while True:
        print("\n************ MENU ************")
        print("1. Minimize Cable Connection Cost")
        print("2. Merge K Sorted Lists")
        print("0. Exit")
        print("******************************")

        choice = input("Select an option: ")
        if choice == '1':
            cables_input = input("Enter cable lengths separated by spaces (or press Enter for random lengths): ")
            if cables_input.strip():
                try:
                    cables = list(map(int, cables_input.split()))
                except ValueError:
                    print("Invalid input. Please enter integers only.")
                    continue
            else:
                cables = [randint(1, 20) for _ in range(10)]
                print(f"Generated random cable lengths: {cables}")

            total_cost = minimize_cable_cost(cables)
            print(f"Minimum cost to connect cables: {total_cost}")

        elif choice == '2':
            lists_input = input("Enter sorted lists separated by semicolons (e.g., 1,4,5;1,3,4;2,6) or press Enter for default: ")
            if lists_input.strip():
                try:
                    lists = [list(map(int, lst.split(','))) for lst in lists_input.split(';')]
                except ValueError:
                    print("Invalid input. Please enter integers only.")
                    continue
            else:
                lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
                print(f"Using default sorted lists: {lists}")

            merged_list = merge_k_lists(lists)
            print(f"Merged Sorted List: {merged_list}")

        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == '__main__':
    main()
