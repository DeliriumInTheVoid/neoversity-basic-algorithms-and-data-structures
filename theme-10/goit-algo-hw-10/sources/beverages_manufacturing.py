from pulp import LpProblem, LpMaximize, LpVariable, lpSum, LpStatus, value
import matplotlib.pyplot as plt
import numpy as np


def optimize_beverage_production():
    prob = LpProblem("Beverage_Production_Optimization", LpMaximize)

    lemonade = LpVariable("Lemonade", lowBound=0, cat='Integer')     # x-axis
    fruit_juice = LpVariable("Fruit_Juice", lowBound=0, cat='Integer') # y-axis

    # lemonade(L) + fruit_juice(J) -> maximize
    prob += lpSum([lemonade, fruit_juice]), "Total_Production"

    # all constraints
    prob += 2 * lemonade + 1 * fruit_juice <= 100, "Water_Constraint"
    prob += 1 * lemonade <= 50, "Sugar_Constraint"
    prob += 1 * lemonade <= 30, "Lemon_Juice_Constraint"
    prob += 2 * fruit_juice <= 40, "Fruit_Puree_Constraint"

    prob.solve()

    print(f"Статус рішення: {LpStatus[prob.status]}")
    print(f"Лимонад (од.): {value(lemonade)}")
    print(f"Фруктовий сік (од.): {value(fruit_juice)}")
    print(f"Всього продуктів: {value(prob.objective)}")

    # visualization
    plt.figure(figsize=(10, 8))
    # lemonade (x) from 0 to 60
    x = np.linspace(0, 60, 400)
    # water constraint: 2L + J <= 100 -> J <= 100 - 2L
    y_water = 100 - 2 * x
    # fruit puree constraint: 2J <= 40 -> J <= 20
    y_puree = np.full_like(x, 20)

    # constraint lines
    plt.plot(x, y_water, label=r'Вода: $2x + y \leq 100$', color='blue')
    plt.plot(x, y_puree, label=r'Пюре: $2y \leq 40 \Rightarrow y \leq 20$', color='green')

    # vertical lines for sugar and lemon juice constraints
    plt.axvline(x=50, color='orange', linestyle='--', label=r'Цукор: $x \leq 50$')
    plt.axvline(x=30, color='red', linestyle='-', label=r'Лимонний сік: $x \leq 30$')

    # feasible region
    y_feasible = np.minimum(y_water, y_puree)

    # all constraints combined
    where_condition = (x <= 30) & (y_feasible >= 0)

    plt.fill_between(x, 0, y_feasible, where=where_condition, color='gray', alpha=0.3, label='Допустима область')

    # optimal point
    opt_x = value(lemonade)
    opt_y = value(fruit_juice)
    plt.plot(opt_x, opt_y, 'ro', markersize=10, label=f'Оптимум ({int(opt_x)}, {int(opt_y)})')

    plt.xlim(0, 60)
    plt.ylim(0, 60)
    plt.xlabel('Лимонад (од.)')
    plt.ylabel('Фруктовий сік (од.)')
    plt.title('Графічне вирішення задачі лінійного програмування')
    plt.legend()
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    optimize_beverage_production()
