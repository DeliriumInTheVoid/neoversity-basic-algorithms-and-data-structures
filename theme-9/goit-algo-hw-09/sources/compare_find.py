import time
from .find_dynamic import find_min_coins
from .find_greedy import find_coins_greedy


def compare_find(coins: list[int], test_amounts: list[int]) -> list[dict[str, float]]:
    """
    Compare the performance of greedy and dynamic programming algorithms
    for finding minimum number of coins.

    Tests both algorithms with various amounts and measures their execution time.
    """

    print("=" * 80)
    print("COIN CHANGE ALGORITHMS COMPARISON")
    print("=" * 80)
    print(f"Coin denominations: {coins}")
    print("=" * 80)

    results = []

    for amount in test_amounts:
        print(f"\nTesting for amount: {amount}")
        print("-" * 80)

        # greedy algorithm
        start_time = time.perf_counter()
        greedy_result = find_coins_greedy(coins, amount)
        greedy_time = time.perf_counter() - start_time
        greedy_total_coins = sum(greedy_result.values())

        print(f"Greedy Algorithm:")
        print(f"  Result: {greedy_result}")
        print(f"  Number of coins: {greedy_total_coins}")
        print(f"  Execution time: {greedy_time:.8f} seconds")

        # dynamic programming algorithm
        start_time = time.perf_counter()
        dp_result = find_min_coins(coins, amount)
        dp_time = time.perf_counter() - start_time
        dp_total_coins = sum(dp_result.values())

        print(f"Dynamic Programming:")
        print(f"  Result: {dp_result}")
        print(f"  Number of coins: {dp_total_coins}")
        print(f"  Execution time: {dp_time:.8f} seconds")

        # compare results
        speedup = dp_time / greedy_time if greedy_time > 0 else 0
        print(f"\nComparison:")
        print(f"  Greedy algorithm is {speedup:.2f}x faster")
        print(f"  Same number of coins: {'Yes' if greedy_total_coins == dp_total_coins else 'No'}")

        results.append({
            'amount': amount,
            'greedy_time': greedy_time,
            'dp_time': dp_time,
            'greedy_coins': greedy_total_coins,
            'dp_coins': dp_total_coins,
            'speedup': speedup
        })

    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"{'Amount':>10} | {'Greedy (s)':>15} | {'Dynamic (s)':>15} | {'Speedup':>12}")
    print("-" * 80)

    for r in results:
        print(f"{r['amount']:>10} | {r['greedy_time']:>15.8f} | {r['dp_time']:>15.8f} | {r['speedup']:>12.2f}x")

    print("=" * 80)

    return results
