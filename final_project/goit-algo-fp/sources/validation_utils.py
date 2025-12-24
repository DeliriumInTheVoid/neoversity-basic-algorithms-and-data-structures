from typing import Tuple


def get_int_value(text:str, default_value:int | None=None, diapason:Tuple[int, int] | None=None) -> int:
    if diapason is None or len(diapason) != 2 or diapason[1] - diapason[0] < 1:
        diapason = (-float("inf"), float("inf"))

    value = input(text)
    try:
        value = int(value)
    except ValueError:
        value = default_value

    if not (diapason[0] <= value <= diapason[1]):
        value = default_value

    return value


def get_mix_max_values():
    min_value = get_int_value("Enter the minimum value [10]: ", default_value=10)
    max_value = get_int_value("Enter the maximum value [100]: ", default_value=100)

    if min_value > max_value:
        print("Min value cannot be greater than max value.")
        return None

    return min_value, max_value


def get_list_values():
    size = get_int_value("Enter the size of List [10]: ",
                         default_value=10, diapason=(1, 1000))

    return size, *get_mix_max_values()
