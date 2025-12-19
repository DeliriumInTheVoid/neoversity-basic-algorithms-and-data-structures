from sources.compare_find import compare_find


def main():
    coins = [50, 25, 10, 5, 2, 1]
    test_amounts = [113, 500, 1000, 5000, 10000]

    compare_find(coins, test_amounts)


if __name__ == "__main__":
    main()
