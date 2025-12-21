import scipy.integrate as spi
import matplotlib.pyplot as plt
import numpy as np
from typing import Callable


class FunctionData:
    def __init__(self, func: Callable[[float], float], a: float, b: float, name: str = "f(x)"):
        self.func = func
        self.a = a
        self.b = b
        self.name = name


def draw_function(func_data: FunctionData):
    margin = (func_data.b - func_data.a) * 0.2
    x_start = func_data.a - margin
    x_end = func_data.b + margin

    x = np.linspace(x_start, x_end, 400)
    y = func_data.func(x)

    fig, ax = plt.subplots(figsize=(8, 5))

    ax.plot(x, y, 'r', linewidth=2, label=func_data.name)

    ix = np.linspace(func_data.a, func_data.b, 100)
    iy = func_data.func(ix)
    ax.fill_between(ix, iy, color='gray', alpha=0.3, label='Область інтегрування')

    ax.set_xlim([x[0], x[-1]])

    y_min, y_max = min(y), max(y)
    y_range = y_max - y_min
    if y_range == 0: y_range = 1.0
    ax.set_ylim([y_min - y_range * 0.1, y_max + y_range * 0.1])

    ax.set_xlabel('x')
    ax.set_ylabel('f(x)')

    ax.axvline(x=func_data.a, color='blue', linestyle='--', alpha=0.6)
    ax.axvline(x=func_data.b, color='blue', linestyle='--', alpha=0.6)

    ax.set_title(f'Інтегрування {func_data.name} від {func_data.a} до {func_data.b}')

    ax.legend()
    plt.grid(True, alpha=0.5)
    plt.show()


def quad_calc(func_data: FunctionData):
    full_result = spi.quad(func_data.func, func_data.a, func_data.b)
    return full_result[0], full_result[1]


def monte_carlo_integration(func_data: FunctionData, num_samples=100_000):
    # random samples
    x_samples = np.random.uniform(func_data.a, func_data.b, num_samples)
    y_samples = func_data.func(x_samples)

    # integral ≈ (b - a) * E[f(x)]
    return (func_data.b - func_data.a) * np.mean(y_samples)
