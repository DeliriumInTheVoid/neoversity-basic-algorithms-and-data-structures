import random
from collections import Counter


ANALYTICAL_COUNTS = {s: c for s, c in zip(range(2, 13), [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])}
ANALYTICAL_PROBS = {s: c / 36 for s, c in ANALYTICAL_COUNTS.items()}


def simulate_two_dice(num_rolls: int, seed: int | None = None) -> dict[int, float]:
    """Return empirical probabilities for sums 2..12 from `num_rolls` simulations."""
    if num_rolls <= 0:
        raise ValueError("num_rolls must be a positive integer")
    if seed is not None:
        random.seed(seed)

    counts = Counter()
    for _ in range(num_rolls):
        d1 = random.randint(1, 6)
        d2 = random.randint(1, 6)
        counts[d1 + d2] += 1

    return {s: counts.get(s, 0) / num_rolls for s in range(2, 13)}


def format_table(empirical: dict[int, float]) -> str:
    header = f"{'Sum':>3} | {'Empirical':>10} | {'Analytical':>10} | {'Diff':>10}"
    sep = "-" * len(header)
    lines = [header, sep]
    for s in range(2, 13):
        emp = empirical[s]
        ana = ANALYTICAL_PROBS[s]
        diff = emp - ana
        lines.append(f"{s:>3} | {emp:>10.6f} | {ana:>10.6f} | {diff:>+10.6f}")
    return "\n".join(lines)


if __name__ == "__main__":
    num_rolls = 1_000_000
    seed = 42

    empirical = simulate_two_dice(num_rolls, seed=seed)
    print(format_table(empirical))
