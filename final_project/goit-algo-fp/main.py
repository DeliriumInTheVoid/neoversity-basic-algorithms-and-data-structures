import json
from sources.linked_list import LinkedList, generate_random_linked_list
from sources.pythagoras_tree import render_tree
from sources.dijkstra_search import paths_dijkstra, create_transportation_network, draw_graph_with_path
from sources.pyramid_visualizer import draw_heap
from sources.binary_tree_bfs_dfs_animation import show_tree_traversal_visualizer
from sources.calories_to_price_optimizer import greedy_algorithm, dynamic_programming
from sources.dices_with_monte_carlo.monte_carlo_dices_analysis import run_analysis

from sources.validation_utils import get_int_value, get_list_values, get_mix_max_values

def main():
    while True:
        print("\n************ MENU ************")
        print("1. Linked List Operations")
        print("2. Pythagoras Binary Tree Visualization")
        print("3. Dijkstra's Shortest Path Visualization")
        print("4. Pyramid Tree Visualization")
        print("5. Binary Tree BFS/DFS Animation")
        print("6. Calories to Price Optimization")
        print("7. Monte Carlo Simulation for Two Dice Sums")
        print("0. Exit")
        print("******************************")
        choice = input("Select an option: ")
        if choice == '1':
            while True:
                print("\n************* Select List Operation *************")
                print("1. Reverse Linked List")
                print("2. Sort Linked List")
                print("3. Merge Two Sorted Linked Lists")
                print("0. Back to Main Menu")
                print("******************************************")

                list_choice = input("Select an operation: ")
                if list_choice == '1':
                    list_size, min_value, max_value = get_list_values()

                    linked_list = generate_random_linked_list(list_size, (min_value, max_value))

                    print("Original Linked List:")
                    print(linked_list)
                    linked_list.reverse_list()
                    print("Reversed Linked List:")
                    print(linked_list)
                elif list_choice == '2':
                    list_size, min_value, max_value = get_list_values()

                    linked_list = generate_random_linked_list(list_size, (min_value, max_value))

                    print("Original Linked List:")
                    print(linked_list)

                    sort_strategy_choice = input(
                        "Select sorting strategy - merge (m), insertion (i), quick (q), bubble (b) [m]: "
                    ).strip().lower() or "m"

                    if sort_strategy_choice == 'i':
                        sort_strategy_choice = "insertion"
                    elif sort_strategy_choice == 'q':
                        sort_strategy_choice = "quick"
                    elif sort_strategy_choice == 'b':
                        sort_strategy_choice = "bubble"
                    else:
                        sort_strategy_choice = "merge"

                    linked_list.sort_list(sort_strategy_choice)
                    print("Sorted Linked List:")
                    print(linked_list)
                elif list_choice == '3':
                    list_size1 = get_int_value("Enter the size of First Sorted Linked List [10]: ",
                                               default_value=10, diapason=(2, 1000))
                    list_size2 = get_int_value("Enter the size of Second Sorted Linked List [15]: ",
                                               default_value=15, diapason=(2, 1000))
                    min_value, max_value = get_mix_max_values()

                    linked_list1 = generate_random_linked_list(list_size1, (min_value, max_value), sorted=True)
                    linked_list2 = generate_random_linked_list(list_size2, (min_value, max_value), sorted=True)
                    print("First Sorted Linked List:")
                    print(linked_list1)
                    print("Second Sorted Linked List:")
                    print(linked_list2)
                    # merged_list = LinkedList.merge_sorted(linked_list1, linked_list2)
                    merged_list = linked_list1.merge_sorted(linked_list2)
                    print("Merged Sorted Linked List:")
                    print(merged_list)
                elif list_choice == '0':
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
        elif choice == '2':
            tree_type = input("Enter tree type (squares/binary) [binary]: ").strip().lower() or "binary"
            if tree_type not in ("squares", "binary"):
                tree_type = "binary"
            depth = get_int_value("Enter recursion depth (1-15) [7]: ", default_value=7, diapason=(1, 15))
            render_tree(tree_type, depth)
        elif choice == '3':
            num_stations = get_int_value("Enter the number of stations [10]: ", default_value=10, diapason=(2, 100))
            num_connections = get_int_value("Enter the number of connections [15]: ",
                                            default_value=15, diapason=(num_stations-1, num_stations*(num_stations-1)//2))
            transportation_network = create_transportation_network(num_stations, num_connections, weights=True)

            start_station = get_int_value("Enter the start station [1]: ",
                                          default_value=1, diapason=(1, num_stations))
            target_station = get_int_value("Enter the target station [2]: ",
                                           default_value=2, diapason=(1, num_stations))

            if start_station == target_station:
                print("Target station cannot be the same as start station.")
                continue

            start_station_name = f"S_{start_station}"
            target_station_name = f"S_{target_station}"

            shortest_paths = paths_dijkstra(transportation_network, start_station_name)
            for node, (distance, path) in shortest_paths.items():
                print(f"From {start_station_name} to {node}: distance = {distance}, path = {' -> '.join(path)}")

            print(f"\nShortest path from {start_station_name} to {target_station_name}: "
                  f"{' -> '.join(shortest_paths[target_station_name][1])}, "
                  f"distance = {shortest_paths[target_station_name][0]}")

            _, path_to_target = shortest_paths[target_station_name]
            draw_graph_with_path(transportation_network, path_to_target,
                                 title=f"Shortest path from {start_station_name} to {target_station_name}")
        elif choice == '4':
            import random
            elements_num = get_int_value("Enter number of elements in the pyramid [15]: ", default_value=15, diapason=(1, 100))
            draw_heap(list(random.sample(range(1, 100), elements_num)), heap_type="min", heapify=True, validate=False)
        elif choice == '5':
            elements_num, min_value, max_value = get_list_values()
            show_tree_traversal_visualizer(elements_num, min_value, max_value)
        elif choice == '6':
            with open("./data/calories_cost.json", "r") as f:
                data = json.load(f)
            print("Loaded data for Calories to Price Optimization.")
            budget = get_int_value("Enter your budget [50]: ", default_value=50, diapason=(1, 1000))
            print(f"Optimizing for a budget of {budget}...\n")
            greedy_res = greedy_algorithm(data, budget)
            dyn_res = dynamic_programming(data, budget)
            print("Greedy Algorithm Result:")
            print(f"Chosen items: {greedy_res.chosen}")
            print(f"Total Cost: {greedy_res.total_cost}")
            print(f"Total Calories: {greedy_res.total_calories}\n")
            print("Dynamic Programming Result:")
            print(f"Chosen items: {dyn_res.chosen}")
            print(f"Total Cost: {dyn_res.total_cost}")
            print(f"Total Calories: {dyn_res.total_calories}")
        elif choice == '7':
            throws_array = input("Enter number of simulated throws "
                                 "(space separated, default '100 1000 10000 1000000'): ") or "100 1000 10000 1000000"
            try:
                throws_list = [int(x) for x in throws_array.split()]
            except ValueError:
                print("Invalid input. Using default values.")
                throws_list = [100, 1000, 10000, 1000000]

            seed = get_int_value("Enter random seed (optional, default 42): ", default_value=42, diapason=(0, 2**31-1))

            print("\n" + "="*60)
            print("Monte Carlo Convergence Analysis")
            print("="*60)

            for num_rolls in throws_list:
                print(f"\nRunning simulation with N={num_rolls:,} rolls (seed={seed})...")
                run_analysis(num_rolls, seed=seed)

        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
