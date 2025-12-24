from dataclasses import dataclass
from typing import Dict, List, Tuple


Items = Dict[str, Dict[str, int]]


@dataclass(frozen=True)
class SelectionResult:
    chosen: List[str]
    total_cost: int
    total_calories: int


def greedy_algorithm(items: Items, budget: int) -> SelectionResult:
    """
    Greedy heuristic for 0/1 knapsack:
    pick items by descending calories-to-cost ratio while staying within budget.
    This is fast but not guaranteed to be optimal.
    """
    if budget < 0:
        raise ValueError("Budget must be non-negative.")

    # Sort by calories/cost ratio (descending). If tie, prefer higher calories, then lower cost.
    ordered = sorted(
        items.items(),
        key=lambda kv: (
            kv[1]["calories"] / kv[1]["cost"],
            kv[1]["calories"],
            -kv[1]["cost"],
        ),
        reverse=True,
    )

    chosen: List[str] = []
    total_cost = 0
    total_calories = 0

    for name, data in ordered:
        cost = data["cost"]
        calories = data["calories"]
        if total_cost + cost <= budget:
            chosen.append(name)
            total_cost += cost
            total_calories += calories

    return SelectionResult(chosen=chosen, total_cost=total_cost, total_calories=total_calories)


def dynamic_programming(items: Items, budget: int) -> SelectionResult:
    """
    Optimal 0/1 knapsack solution using dynamic programming.
    dp[i][b] = maximum calories using first i items with budget b.
    Also reconstructs the chosen items.
    """
    if budget < 0:
        raise ValueError("Budget must be non-negative.")

    names = list(items.keys())
    n = len(names)

    dp = [[0] * (budget + 1) for _ in range(n + 1)]
    take = [[False] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name = names[i - 1]
        cost_i = items[name]["cost"]
        cal_i = items[name]["calories"]

        for b in range(budget + 1):
            best = dp[i - 1][b]

            if cost_i <= b:
                alt = dp[i - 1][b - cost_i] + cal_i
                if alt > best:
                    best = alt
                    take[i][b] = True

            dp[i][b] = best

    # Reconstruct chosen items
    chosen: List[str] = []
    b = budget
    for i in range(n, 0, -1):
        if take[i][b]:
            name = names[i - 1]
            chosen.append(name)
            b -= items[name]["cost"]

    chosen.reverse()

    total_cost = sum(items[name]["cost"] for name in chosen)
    total_calories = sum(items[name]["calories"] for name in chosen)

    return SelectionResult(chosen=chosen, total_cost=total_cost, total_calories=total_calories)


if __name__ == "__main__":
    items = {
        "pizza": {"cost": 50, "calories": 300},
        "hamburger": {"cost": 40, "calories": 250},
        "hot-dog": {"cost": 30, "calories": 200},
        "pepsi": {"cost": 10, "calories": 100},
        "cola": {"cost": 15, "calories": 220},
        "potato": {"cost": 25, "calories": 350},
    }

    budget = 100

    greedy_res = greedy_algorithm(items, budget)
    dp_res = dynamic_programming(items, budget)

    print("Budget:", budget)
    print("Greedy:", greedy_res)
    print("DP:", dp_res)
