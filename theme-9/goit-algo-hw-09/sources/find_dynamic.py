def find_min_coins(coins: list[int], amount: int) -> dict[int, int]:
    """
    Finds the minimum number of coins needed to make the given amount using dynamic programming.
    Args:
        coins (list[int]): List of coin denominations available.
        amount (int): The target amount to make change for.
    Returns:
        dict[int, int]: A dictionary with coin denominations as keys and their counts as values.
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

    # array to store the minimum coins needed for each amount
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0  # Base case: 0 coins are needed to make amount 0

    # array to store the last coin used to make each amount
    last_coin = [-1] * (amount + 1)

    for coin in coins:
        for x in range(coin, amount + 1):
            if dp[x - coin] + 1 < dp[x]:
                dp[x] = dp[x - coin] + 1
                last_coin[x] = coin

    if dp[amount] == float('inf'):
        return {}

    result = {}
    while amount > 0:
        coin = last_coin[amount]
        if coin in result:
            result[coin] += 1
        else:
            result[coin] = 1
        amount -= coin
    return result


if __name__ == '__main__':
    coin_denominations = [1, 2, 5, 10, 20, 50]
    target_amount = 113
    result = find_min_coins(coin_denominations, target_amount)
    print(f"Minimum coins to make {target_amount}: {result}")
