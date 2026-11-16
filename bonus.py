import sys
import matplotlib.pyplot as plt
from utils import load_csv
from predict import get_estimation, get_thetas

def plot_regresion(theta0, theta1, x_data, y_data):
    try:
        min_x = min(x_data)
        max_x = max(x_data)

        line_x_min = get_estimation(theta0=theta0, theta1=theta1, milleage=min_x)
        line_x_max = get_estimation(theta0=theta0, theta1=theta1, milleage=max_x)

        plt.plot([min_x, max_x], [line_x_min, line_x_max], color='red', label=f'line regression: y = {theta0:.2f} + {theta1:.2f}x', linewidth=2)
        plt.scatter(x_data, y_data, color='blue', label='Real data (data.csv)', zorder=5)
        plt.title('ft_linear_regression - Price vs Milleage', fontsize=14, fontweight='bold')
        plt.xlabel('Milleage (km)', fontsize=12)
        plt.ylabel('Price (€)', fontsize=12)
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.show()
    except Exception as e:
        print(f"[ERROR] Cant generate grafic representation: {e}")
        sys.exit(1)

def main():
    theta0, theta1 = get_thetas()
    x_data, y_data = load_csv()
    if not x_data or not y_data:
        print(f"[ERROR] The data could not be retrieved from data.csv aborting bonus... ")
        sys.exit(1)
    else:
        plot_regresion(theta0=theta0, theta1=theta1, x_data=x_data, y_data=y_data)

if __name__ == "__main__":
    main()