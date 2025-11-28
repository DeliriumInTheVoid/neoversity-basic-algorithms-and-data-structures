from pack import should_exclude
from sources.files_sorter import sort_files
from sources.koch_snowflake import draw_snowflake
from sources.hanoi_tower import hanoi_tower


def main():
    while True:
        print("\n************ MENU ************")
        print("1. File Sorter")
        print("2. Koch Snowflake")
        print("3. Hanoi Tower")
        print("0. Exit")
        print("******************************")
        try:
            choice = int(input("Select an option: "))
            if choice == 1:
                source_dir = input("Enter the source directory path: ")
                dest_dir = input("Enter the destination directory path (default is 'dist'): ")

                try:
                    sort_files(source_dir, dest_dir)
                    print(f"Files from {source_dir} have been sorted into {dest_dir}.")
                except Exception as e:
                    print(f"An error occurred: {e}")
            elif choice == 2:
                order = int(input("Enter the recursion level (e.g., 0-5): "))
                if order < 0:
                    print("Recursion level must be a non-negative integer.")
                    continue
                if order == 0:
                    print("A Koch snowflake of order 0 is just an equilateral triangle.")
                if order > 6:
                    print("Warning: High recursion levels may take a long time to draw.")
                    should_continue = input("Do you want to continue? (y/n): ")
                    if should_continue.lower() != 'y':
                        continue

                size = 300
                draw_snowflake(order, size)
            elif choice == 3:
                n = int(input("Введіть кількість дисків: "))
                rods = {
                    'A': list(range(n, 0, -1)),
                    'B': [],
                    'C': []
                }
                print(f"Початковий стан: {rods}")
                hanoi_tower(n, 'A', 'C', 'B', rods)
                print(f"Кінцевий стан: {rods}")

            elif choice == 0:
                print("Exiting the program.")
                break
            else:
                print("Invalid choice. Please select a valid option.")
        except Exception as e:
            print(f"An error occurred: {e}")


if __name__ == '__main__':
    main()
