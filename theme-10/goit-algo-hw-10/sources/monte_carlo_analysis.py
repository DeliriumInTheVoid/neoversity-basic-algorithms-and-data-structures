import numpy as np
from .monte_carlo_integration import FunctionData, quad_calc, monte_carlo_integration


def run_comparative_analysis():
    """Run comparative analysis for different sample sizes and functions"""

    functions = [
        FunctionData(
            func=lambda x: x**2,
            a=0,
            b=1,
            name="x^2"
        ),
        FunctionData(
            func=lambda x: np.sin(x),
            a=0,
            b=np.pi,
            name="sin(x)"
        ),
        FunctionData(
            func=lambda x: np.exp(x),
            a=0,
            b=1,
            name="e^x"
        )
    ]

    sample_sizes = [1000, 100000, 1000000]

    print("=" * 80)
    print("COMPARATIVE ANALYSIS: Monte Carlo Integration vs Quad Method")
    print("=" * 80)

    for func_data in functions:
        print(f"\n\nFunction: {func_data.name} from {func_data.a} to {func_data.b}")
        print("-" * 80)

        quad_result, quad_error = quad_calc(func_data)
        print(f"Analytical Result (quad): {quad_result:.10f} ± {quad_error:.2e}")
        print()

        for num_samples in sample_sizes:
            runs = 10
            mc_results = []

            for _ in range(runs):
                mc_result = monte_carlo_integration(func_data, num_samples)
                mc_results.append(mc_result)

            mc_mean = np.mean(mc_results)
            mc_std = np.std(mc_results)
            absolute_error = abs(quad_result - mc_mean)
            relative_error = (absolute_error / quad_result) * 100

            print(f"Sample Size: {num_samples:>10,}")
            print(f"  Monte Carlo Mean:     {mc_mean:.10f}")
            print(f"  Monte Carlo Std Dev:  {mc_std:.10f}")
            print(f"  Absolute Error:       {absolute_error:.10f}")
            print(f"  Relative Error:       {relative_error:.6f}%")
            print()

    print("=" * 80)
    print("Analysis Complete")
    print("=" * 80)


if __name__ == "__main__":
    run_comparative_analysis()
