import math


def calculate_complexity_ratio(data, algorithm):
    """
    Calculate empirical complexity ratio to determine O(f(n))
    For linear O(n): ratio should be proportional to n increase
    For O(n log n): ratio should be proportional to n*log(n) increase
    """
    sizes = [int(s) for s in data['sizes']]
    times = data[algorithm]

    print(f"\n{algorithm.upper()} Complexity Analysis:")
    print("-" * 60)

    for i in range(1, len(sizes)):
        size_ratio = sizes[i] / sizes[i-1]
        time_ratio = times[i] / times[i-1] if times[i-1] > 0 else 0

        expected_linear = size_ratio
        expected_n_log_n = (sizes[i] * math.log(sizes[i])) / (sizes[i-1] * math.log(sizes[i-1]))

        linear_fit = time_ratio / expected_linear
        n_log_n_fit = time_ratio / expected_n_log_n

        print(f"  {sizes[i-1]:>6} -> {sizes[i]:>6} chars:")
        print(f"    Size increase: {size_ratio:.2f}x")
        print(f"    Time increase: {time_ratio:.2f}x")
        print(f"    O(n) fit:      {linear_fit:.2f} (1.0 = perfect linear)")
        print(f"    O(n log n) fit: {n_log_n_fit:.2f}")

        # best fit
        if abs(linear_fit - 1.0) < 0.2:
            print(f"    Best fit: O(n) - Linear complexity")
        elif linear_fit < 0.8:
            print(f"    Best fit: O(n/m) - Sublinear (pattern skipping)")
        else:
            print(f"    Best fit: O(n log n) or higher")


def calculate_average_constant_factor(data, algorithm, baseline_algorithm='boyer_moore'):
    baseline_times = data[baseline_algorithm]
    algo_times = data[algorithm]

    ratios = [algo_times[i] / baseline_times[i] if baseline_times[i] > 0 else 0
              for i in range(len(baseline_times))]

    avg_ratio = sum(ratios) / len(ratios)
    return avg_ratio


def comprehensive_analysis(data):
    print("=" * 80)
    print("COMPREHENSIVE STRING SEARCH ALGORITHMS ANALYSIS")
    print("=" * 80)

    for scenario in ['existing', 'non_existing']:
        print(f"\n\n{'='*80}")
        print(f"SCENARIO: Pattern {'EXISTS' if scenario == 'existing' else 'DOES NOT EXIST'}")
        print("=" * 80)

        scenario_data = data[scenario]

        for algorithm in ['boyer_moore', 'kmp', 'rabin_karp']:
            calculate_complexity_ratio(scenario_data, algorithm)

        print(f"\n\nPERFORMANCE COMPARISON (relative to Boyer-Moore):")
        print("-" * 60)

        for algorithm in ['kmp', 'rabin_karp']:
            avg_factor = calculate_average_constant_factor(scenario_data, algorithm)
            print(f"  {algorithm.upper():12} is {avg_factor:.2f}x slower on average")

        print(f"\n\nEFFICIENCY AT DIFFERENT SCALES:")
        print("-" * 60)
        sizes = scenario_data['sizes']
        for i, size in enumerate(sizes):
            print(f"\n  Text size: {size} characters")
            bm_time = scenario_data['boyer_moore'][i]
            kmp_time = scenario_data['kmp'][i]
            rk_time = scenario_data['rabin_karp'][i]

            # time per character
            size_int = int(size)
            bm_per_char = (bm_time / size_int) * 1000000  # microseconds per char
            kmp_per_char = (kmp_time / size_int) * 1000000
            rk_per_char = (rk_time / size_int) * 1000000

            print(f"    Boyer-Moore:  {bm_time:.6f}s total, {bm_per_char:.3f} us/char")
            print(f"    KMP:          {kmp_time:.6f}s total, {kmp_per_char:.3f} us/char ({kmp_time/bm_time:.2f}x)")
            print(f"    Rabin-Karp:   {rk_time:.6f}s total, {rk_per_char:.3f} us/char ({rk_time/bm_time:.2f}x)")


def generate_summary_table(data):
    print("\n\n" + "=" * 80)
    print("SUMMARY TABLE")
    print("=" * 80)

    print("\nPattern EXISTS in text:")
    print("-" * 80)
    print(f"{'Size':<10} | {'Boyer-Moore':<11} | {'KMP':<11} | {'Rabin-Karp':<11} | {'Winner':<11}")
    print("-" * 80)

    for i, size in enumerate(data['existing']['sizes']):
        bm = data['existing']['boyer_moore'][i]
        kmp = data['existing']['kmp'][i]
        rk = data['existing']['rabin_karp'][i]
        winner = min([('BM', bm), ('KMP', kmp), ('RK', rk)], key=lambda x: x[1])[0]
        print(f"{size:<10} | {bm:>10.6f}s | {kmp:>10.6f}s | {rk:>10.6f}s | {winner:<12}")

    print("\nPattern DOES NOT EXIST in text:")
    print("-" * 80)
    print(f"{'Size':<10} | {'Boyer-Moore':<11} | {'KMP':<11} | {'Rabin-Karp':<11} | {'Winner':<11}")
    print("-" * 80)

    for i, size in enumerate(data['non_existing']['sizes']):
        bm = data['non_existing']['boyer_moore'][i]
        kmp = data['non_existing']['kmp'][i]
        rk = data['non_existing']['rabin_karp'][i]
        winner = min([('BM', bm), ('KMP', kmp), ('RK', rk)], key=lambda x: x[1])[0]
        print(f"{size:<10} | {bm:>10.6f}s | {kmp:>10.6f}s | {rk:>10.6f}s | {winner:<12}")
