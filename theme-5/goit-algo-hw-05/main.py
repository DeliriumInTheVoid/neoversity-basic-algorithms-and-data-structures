from sources.hash_table import HashTable
from sources.binary_search import binary_search
from sources.sub_str_search import compare_sub_str_search as sub_str_search
from sources.sub_str_search import analyze_results as analysis


def search_sub_srt_analysis():
    print("=" * 100)
    print("STRING SEARCH ALGORITHMS PERFORMANCE COMPARISON")
    print("=" * 100)

    pattern = "algorithm"
    text_sizes = [1000, 10000, 50000, 100000]
    iterations_list = [1000, 500, 100, 50]  # iterations for larger texts

    print(f"\nTest Configuration:")
    print(f"  Pattern: '{pattern}' (length: {len(pattern)})")
    print(f"  Text sizes: {text_sizes}")
    print(f"  Iterations per size: {iterations_list}")

    results = sub_str_search.run_benchmarks(text_sizes, pattern, iterations_list)
    sub_str_search.print_results(results)
    sub_str_search.analyze_complexity(results)

    data = sub_str_search.process_data(results)

    analysis.comprehensive_analysis(data)
    analysis.generate_summary_table(data)

    print("\n\n" + "=" * 80)
    print("CONCLUSIONS")
    print("=" * 80)
    print("""
       1. BOYER-MOORE demonstrates SUBLINEAR behavior (O(n/m)) in practice:
          - Shows near-constant time for large texts
          - Most efficient for single-pattern search
          - 2-6x faster than alternatives

       2. KMP shows perfect LINEAR behavior (O(n+m)):
          - Consistent scaling proportional to text size
          - Predictable performance
          - Good for worst-case guarantees

       3. RABIN-KARP shows LINEAR behavior (O(n+m)) with HIGH constants:
          - Hash computation overhead dominates
          - 5-6x slower than Boyer-Moore
          - Better suited for multi-pattern search

       RECOMMENDATION: Use Boyer-Moore for single-pattern text search!
           """)
    print("=" * 80)


def main():
    while True:
        print("\n************ MENU ************")
        print("1. Hash Table Demo")
        print("2. Binary Search Demo")
        print("3. String Search Algorithms Analysis")
        print("0. Exit")
        print("******************************")

        choice = input("Select an option: ")

        if choice == '1':
            ht = HashTable(5)
            ht.insert("apple", 10)
            ht.insert("orange", 20)
            ht.insert("banana", 30)

            print(f"HashTable state after inserts: {ht.table}")
            print(f"Get 'apple': {ht.get('apple')}")
            ht.delete("apple")
            print(f"HashTable state after deleting 'apple': {ht.table}")
            print(f"Get 'apple' after deletion: {ht.get('apple')}")
        elif choice == '2':
            array = [1.1, 2.3, 3.5, 4.7, 5.9, 6.0, 7.2]
            print(f"Array state after insertion: {array}")
            number = input("Enter a number to search: ")
            try:
                number = float(number)
                iterations, upper_bound = binary_search(array, number)
                print(f"Iterations: {iterations}, Upper Bound: {upper_bound}")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif choice == '3':
            search_sub_srt_analysis()
            input("Press any key to continue...")
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == '__main__':
    main()
