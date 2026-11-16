import json
import sys
import os
import matplotlib.pyplot as plt
import csv
from utils import print_box, CheckImput, InvalidMielleageError, parse_arguments, CSV_FILEPATH, THETA_FILEPATH, load_csv


def get_thetas():
    theta0, theta1 = 0.0, 0.0
    if os.path.exists(THETA_FILEPATH):
        try:
            print(f"{THETA_FILEPATH} detected")
            with open(THETA_FILEPATH, "r") as f:
                data_theta = json.load(f)
                raw_theta0 = data_theta.get("theta0") 
                raw_theta1 = data_theta.get("theta1")
                if raw_theta0 is None or raw_theta1 is None:
                    print(f"[ERROR] the keys theta0 or theta1 were not found in {THETA_FILEPATH}.")
                    print(f"Using base values...")
                    return 0.0, 0.0
                try:
                    theta0 = float(data_theta.get("theta0"))
                    theta1 = float(data_theta.get("theta1"))
                except (ValueError, TypeError) as e:
                    print(f"[ERROR] Invalid format in file {THETA_FILEPATH}")
                    print(f"Values in File are:")
                    print(f"theta0 -> {raw_theta0}")
                    print(f"theta1 -> {raw_theta1}")
                    print(f"Using base values...")
                    return 0.0, 0.0
        except PermissionError:
            print(f"[ERROR] The file ({THETA_FILEPATH}) doesn't have the required permision,")
            print(f"Using base values...")
            return 0.0, 0.0
        except json.JSONDecodeError:
            print(f"[ERROR] The file ({THETA_FILEPATH}) doesn't have the correct format")
            print(f"Using base values...")
            return 0.0, 0.0
        except Exception as e:
            print(f"[UNESPECTED ERROR] An error occurred while reading the file")
            print(f"Using base values...")
            return 0.0, 0.0
    else:
        print(f"{THETA_FILEPATH} no detected")
        print(f"Using base values...")
    return theta0, theta1
        
def get_estimation(theta0, theta1, milleage):
    estimation = theta0 + (theta1 * milleage)
    return round(estimation, 2)


def main():
    args = parse_arguments()
    milleage = CheckImput()
    theta0, theta1 = get_thetas()
    estimation = get_estimation(theta0=theta0, theta1=theta1, milleage=milleage)
    print_box(
        "= RESULTS =",
        "---",
        f"milleage: {milleage} km",
        f"theta0: {theta0}",
        f"theta1: {theta1}",
        f"Estimation price: {estimation} €"
    )
    if args.grafic:
        print(f"[BONUS] Please use 'make bonus' (bonus.py) to display the graphical representation.")


if __name__ == "__main__":
    main()