def find_coins_greedy(coins: list[int], amount: int) -> dict[int, int]:
    """
    Find the minimum number of coins needed to make up a given amount using a greedy algorithm.
    Args:
        coins (list[int]): A list of coin denominations (positive integers).
        amount (int): The target amount to make change for (positive integer).
    Returns:
        dict[int, int]: A dictionary where keys are coin denominations and values are the counts of each coin used.
    Raises:
        ValueError: If the amount is not a positive integer, if the coins list is empty,
                    if any coin denomination is not a positive integer,
                    if the smallest coin denomination is larger than the amount,
                    or if the amount cannot be made with the given coin denominations.
    """
    if amount <= 0:
        raise ValueError("Amount must be a positive integer")
    if not coins:
        raise ValueError("Coin denominations list cannot be empty")

    min_denomination = min(coins)
    if min_denomination <= 0:
        raise ValueError("Coin denominations must be positive integers")
    if min_denomination > amount:
        raise ValueError("The smallest coin denomination is larger than the amount")

    coin_count = {}
    remaining_amount = amount

    for coin in coins:
        count = remaining_amount // coin
        if count > 0:
            coin_count[coin] = count
            remaining_amount -= coin * count

        if remaining_amount == 0:
            break

    if remaining_amount > 0:
        raise ValueError("The amount cannot be made with the given coin denominations")

    return coin_count


if __name__ == "__main__":
    denominations = [50, 25, 10, 5, 2, 1]
    target_amount = 113
    result = find_coins_greedy(denominations, target_amount)
    print(f"Coins used to make {target_amount}: {result}")
