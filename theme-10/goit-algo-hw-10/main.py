import numpy as np
from sources.beverages_manufacturing import optimize_beverage_production
from sources.monte_carlo_integration import FunctionData, draw_function, quad_calc, monte_carlo_integration
from sources.monte_carlo_analysis import run_comparative_analysis

def main():
    while True:
        print("\n************ MENU ************")
        print("1. Beverage Manufacturing Optimization")
        print("2. Monte Carlo Integration")
        print("3. Run Comparative Analysis for Monte Carlo Integration")
        print("0. Exit")
        print("******************************")
        choice = input("Select an option: ")
        if choice == '1':
            optimize_beverage_production()
        elif choice == '2':
            while True:
                print("\n************* Select Function *************")
                print("1. f(x) = x^2")
                print("2. f(x) = sin(x)")
                print("3. f(x) = e^x")
                print("0. Back to Main Menu")
                print("******************************************")
                func_choice = input("Select a function: ")
                if func_choice == '1':
                    func_data = FunctionData(
                        func=lambda x: x**2,
                        a=0,
                        b=1,
                        name="x^2"
                    )
                elif func_choice == '2':
                    func_data = FunctionData(
                        func=lambda x: np.sin(x),
                        a=0,
                        b=np.pi,
                        name="sin(x)"
                    )
                elif func_choice == '3':
                    func_data = FunctionData(
                        func=lambda x: np.exp(x),
                        a=0,
                        b=1,
                        name="e^x"
                    )
                elif func_choice == '0':
                    break
                else:
                    print("Invalid choice. Please select a valid option.")
                    continue
                draw_function(func_data)
                quad_area, error = quad_calc(func_data)
                monte_carlo_area = monte_carlo_integration(func_data)
                print(f"\nResults for integrating f(x) = {func_data.name} from {func_data.a} to {func_data.b}:")
                print(f"Quadrature Method Area: {quad_area} with estimated error {error}")
                print(f"Monte Carlo Integration Area: {monte_carlo_area}\n")
                print(f"Difference between methods: {abs(quad_area - monte_carlo_area)}")
        elif choice == '3':
            run_comparative_analysis()
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please select a valid option.")


if __name__ == "__main__":
    main()
