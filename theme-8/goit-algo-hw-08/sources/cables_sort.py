import heapq

def minimize_cable_cost(cables: list[int]) -> int:
    heapq.heapify(cables)
    total_cost: int = 0

    while len(cables) > 1:
        first = heapq.heappop(cables)
        second = heapq.heappop(cables)

        cost = first + second
        total_cost += cost

        heapq.heappush(cables, cost)

    return total_cost


if __name__ == "__main__":
    cables = [4, 3, 2, 6]
    print("Minimum cost to connect cables:", minimize_cable_cost(cables))  # 29
