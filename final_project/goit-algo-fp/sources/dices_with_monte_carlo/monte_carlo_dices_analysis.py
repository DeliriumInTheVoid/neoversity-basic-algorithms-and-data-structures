from pathlib import Path
import math
import matplotlib.pyplot as plt

from .monte_carlo_dice import simulate_two_dice, format_table, ANALYTICAL_PROBS


def run_analysis(num_rolls: int, seed: int | None = None) -> None:
    empirical = simulate_two_dice(num_rolls, seed=seed)
    print(format_table(empirical))

    analytical = ANALYTICAL_PROBS

    # summary error metrics
    abs_errors = {s: abs(empirical[s] - analytical[s]) for s in range(2, 13)}
    max_abs_error = max(abs_errors.values())
    rmse = math.sqrt(sum((empirical[s] - analytical[s]) ** 2 for s in range(2, 13)) / 11)

    # table
    header = f"{'Sum':>3} | {'Empirical':>10} | {'Analytical':>10} | {'AbsErr':>10}"
    sep = "-" * len(header)
    lines = [header, sep]
    for s in range(2, 13):
        lines.append(f"{s:>3} | {empirical[s]:>10.6f} | {analytical[s]:>10.6f} | {abs_errors[s]:>10.6f}")
    print("\n".join(lines))
    print(f"\nN={num_rolls:,}  max_abs_error={max_abs_error:.6f}  RMSE={rmse:.6f}")

    # plot
    sums = list(range(2, 13))
    emp_vals = [empirical[s] for s in sums]
    ana_vals = [analytical[s] for s in sums]

    plt.figure(figsize=(10, 5))
    x = list(range(len(sums)))
    bar_w = 0.42
    plt.bar([i - bar_w / 2 for i in x], ana_vals, width=bar_w, label="Analytical")
    plt.bar([i + bar_w / 2 for i in x], emp_vals, width=bar_w, label="Monte Carlo")
    plt.xticks(x, sums)
    plt.xlabel("Sum of two dice")
    plt.ylabel("Probability")
    plt.title(f"Two Dice Sum Probabilities (Monte Carlo vs Analytical), N={num_rolls:,}")
    plt.legend()
    plt.tight_layout()
    # show plot
    plt.show()

    # save plot to file
    # plot_path = Path("./dice_probabilities.png")
    # plt.savefig(plot_path, dpi=160)
    # plt.close()


if __name__ == "__main__":
    run_analysis(num_rolls=1_000_000, seed=42)
