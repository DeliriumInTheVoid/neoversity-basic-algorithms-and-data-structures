import timeit
import random
import string
from dataclasses import dataclass
from typing import Dict, List

from .boyer_moore import boyer_moore_search
from .knuth_morris_pratt import kmp_search
from .rabin_karp import rabin_karp_search


@dataclass
class BenchmarkResult:
    text_size: int
    pattern_size: int
    pattern_exists: bool
    boyer_moore_time: float
    kmp_time: float
    rabin_karp_time: float
    iterations: int


def generate_random_string(length):
    return ''.join(random.choices(string.ascii_lowercase + ' ', k=length))


def generate_test_text(size: int, pattern: str, pattern_exists: bool) -> str:
    if pattern_exists:
        # place pattern near the end to test worst-case scenarios
        prefix = generate_random_string(size - len(pattern) - 100)
        suffix = generate_random_string(100)
        return prefix + pattern + suffix
    else:
        return generate_random_string(size)


def benchmark_algorithm(algorithm, text: str, pattern: str, iterations: int) -> float:
    return timeit.timeit(lambda: algorithm(text, pattern), number=iterations)


def run_benchmarks(text_sizes: List[int], pattern: str, iterations_list: List[int]) -> Dict[str, List[BenchmarkResult]]:
    results = {
        'existing': [],
        'non_existing': []
    }

    for text_size, iterations in zip(text_sizes, iterations_list):
        print(f"\nBenchmarking text size: {text_size} characters ({iterations} iterations)")

        text_existing = generate_test_text(text_size, pattern, True)
        print(f"  Testing with existing pattern...")

        bm_time_existing = benchmark_algorithm(boyer_moore_search, text_existing, pattern, iterations)
        kmp_time_existing = benchmark_algorithm(kmp_search, text_existing, pattern, iterations)
        rk_time_existing = benchmark_algorithm(rabin_karp_search, text_existing, pattern, iterations)

        results['existing'].append(BenchmarkResult(
            text_size=text_size,
            pattern_size=len(pattern),
            pattern_exists=True,
            boyer_moore_time=bm_time_existing,
            kmp_time=kmp_time_existing,
            rabin_karp_time=rk_time_existing,
            iterations=iterations
        ))

        print(f"  Testing with non-existing pattern...")
        non_existing_pattern = "xyzzyx" * (len(pattern) // 6 + 1)
        non_existing_pattern = non_existing_pattern[:len(pattern)]
        text_non_existing = generate_test_text(text_size, pattern, False)

        bm_time_non_existing = benchmark_algorithm(boyer_moore_search, text_non_existing, non_existing_pattern, iterations)
        kmp_time_non_existing = benchmark_algorithm(kmp_search, text_non_existing, non_existing_pattern, iterations)
        rk_time_non_existing = benchmark_algorithm(rabin_karp_search, text_non_existing, non_existing_pattern, iterations)

        results['non_existing'].append(BenchmarkResult(
            text_size=text_size,
            pattern_size=len(non_existing_pattern),
            pattern_exists=False,
            boyer_moore_time=bm_time_non_existing,
            kmp_time=kmp_time_non_existing,
            rabin_karp_time=rk_time_non_existing,
            iterations=iterations
        ))

        print(f"    Boyer-Moore: {bm_time_existing:.6f}s (existing), {bm_time_non_existing:.6f}s (non-existing)")
        print(f"    KMP: {kmp_time_existing:.6f}s (existing), {kmp_time_non_existing:.6f}s (non-existing)")
        print(f"    Rabin-Karp: {rk_time_existing:.6f}s (existing), {rk_time_non_existing:.6f}s (non-existing)")

    return results


def print_results(results: Dict[str, List[BenchmarkResult]]):
    print("\n" + "="*100)
    print("BENCHMARK RESULTS")
    print("="*100)

    for scenario, benchmark_list in results.items():
        print(f"\n{'Pattern Exists' if scenario == 'existing' else 'Pattern Does NOT Exist'}")
        print("-" * 100)
        print(f"{'Text Size':<12} | {'Boyer-Moore':<14} | {'KMP':<14} | {'Rabin-Karp':<14} | {'Fastest':<14}")
        print("-" * 100)

        for result in benchmark_list:
            bm = result.boyer_moore_time
            kmp = result.kmp_time
            rk = result.rabin_karp_time

            times = {'Boyer-Moore': bm, 'KMP': kmp, 'Rabin-Karp': rk}
            fastest = min(times, key=times.get)

            print(f"{result.text_size:<12} | {bm:>13.6f}s | {kmp:>13.6f}s | {rk:>13.6f}s | {fastest:<15}")

    print("="*100)


def analyze_complexity(results: Dict[str, List[BenchmarkResult]]):
    print("\n" + "="*100)
    print("COMPLEXITY ANALYSIS")
    print("="*100)

    for scenario, benchmark_list in results.items():
        if len(benchmark_list) < 2:
            continue

        print(f"\n{'Pattern Exists' if scenario == 'existing' else 'Pattern Does NOT Exist'}")
        print("-" * 100)

        for i in range(1, len(benchmark_list)):
            prev = benchmark_list[i-1]
            curr = benchmark_list[i]

            size_ratio = curr.text_size / prev.text_size

            bm_ratio = curr.boyer_moore_time / prev.boyer_moore_time if prev.boyer_moore_time > 0 else 0
            kmp_ratio = curr.kmp_time / prev.kmp_time if prev.kmp_time > 0 else 0
            rk_ratio = curr.rabin_karp_time / prev.rabin_karp_time if prev.rabin_karp_time > 0 else 0

            print(f"\nText size: {prev.text_size} → {curr.text_size} ({size_ratio:.2f}x increase)")
            print(f"  Boyer-Moore time increased: {bm_ratio:.2f}x")
            print(f"  KMP time increased: {kmp_ratio:.2f}x")
            print(f"  Rabin-Karp time increased: {rk_ratio:.2f}x")

    print("\n" + "="*100)


def process_data(results: Dict[str, List[BenchmarkResult]]) -> dict:
    data = {
        'existing': {},
        'non_existing': {}
    }

    for scenario in ['existing', 'non_existing']:
        sizes = []
        bm_times = []
        kmp_times = []
        rk_times = []

        for result in results[scenario]:
            sizes.append(str(result.text_size))
            bm_times.append(round(result.boyer_moore_time, 6))
            kmp_times.append(round(result.kmp_time, 6))
            rk_times.append(round(result.rabin_karp_time, 6))

        data[scenario] = {
            'sizes': sizes,
            'boyer_moore': bm_times,
            'kmp': kmp_times,
            'rabin_karp': rk_times
        }

    return data
