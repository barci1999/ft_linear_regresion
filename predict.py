import json
import sys
import os
import matplotlib.pyplot as plt
import csv
from utils import print_box ,CheckImput,InvalidMielleageError,parse_arguments

THETA_FILEPATH = "theta.json"
CSV_FILEPATH = "data.csv"

def get_thetas():
    theta0,theta1 = 0.0,0.0
    if os.path.exists(THETA_FILEPATH):
        try:
            print(f"{THETA_FILEPATH}  detected")
            with open(THETA_FILEPATH ,"r") as f:
                data_theta = json.load(f)
                raw_theta0 = data_theta.get("theta0") 
                raw_theta1 = data_theta.get("theta1")
                if raw_theta0 is None or raw_theta1 is None:
                    print(f"[ERROR] the keys theta0 or theta1 were not found in {THETA_FILEPATH}.")
                    print(f"Using base values...")
                    return 0.0,0.0
                try:
                    theta0 = float(data_theta.get("theta0"))
                    theta1 = float(data_theta.get("theta1"))
                except (ValueError,TypeError) as e:
                    print(f"[ERROR] Invalid format in file {THETA_FILEPATH}")
                    print(f"Values in File are:")
                    print(f"theta0 -> {raw_theta0}")
                    print(f"theta1 -> {raw_theta1}")
                    print(f"Using base values...")
                    return 0.0,0.0
        except PermissionError:
            print(f"[ERROR] The file ({THETA_FILEPATH}) doesn't have the required permision,")
            print(f"Using base values...")
            return 0.0,0.0
        except json.JSONDecodeError:
            print(f"[ERROR] The file ({THETA_FILEPATH}) doesn't have the correct format")
            print(f"Using base values...")
            return 0.0,0.0
        except Exception as e:
            print(f"[UNESPECTED ERROR] An error occurred while reading the file")
            print(f"Using base values...")
            return 0.0,0.0
    else:
        print(f"{THETA_FILEPATH} no deteacted")
        print(f"Using base values...")
    return(theta0,theta1)
        
def get_estimation(theta0,theta1,milleage):

    estimation = theta0 + (theta1 * milleage)
    return(round(estimation,2))


def load_csv():
    x_data = []
    y_data = []
    
    try:
        with open(CSV_FILEPATH, mode='r') as file:
            reader = csv.DictReader(file)
            
            expected_headers = {'km', 'price'}
            actual_headers = set(reader.fieldnames) if reader.fieldnames else set()
            
            if actual_headers != expected_headers:
                raise ValueError(f"Invalid headers. Expected exactly: {expected_headers}, but found: {actual_headers}")
            
            for line_num, row in enumerate(reader, start=2):
                if len(row) != 2:
                    raise ValueError(f"Invalid format at line {line_num}: expected 2 values ('km', 'price'), but found {len(row)}.")
                try:
                    x_val = float(row['km'])
                    y_val = float(row['price'])
                    
                    x_data.append(x_val)
                    y_data.append(y_val)
                except (ValueError, TypeError):
                    raise ValueError(f"Invalid format at line {line_num}: expected numbers for 'km' and 'price'.")
    except FileNotFoundError:
        print(f"[ERROR] File '{CSV_FILEPATH}' not found.")
        return [], []
    except Exception as e:
        print(f"[CSV FORMAT ERROR]: {e}")
        return [], []
        
    return x_data, y_data
def main():

    args = parse_arguments()
    milleage = CheckImput()
    theta0,theta1 = get_thetas()
    estimation = get_estimation(theta0=theta0,theta1=theta1,milleage=milleage)
    print_box(
        "= RESULTS =",
        "---",
        f"milleage: {milleage} km",
        f"theta0: {theta0}",
        f"theta1: {theta1}",
        f"Estimation price: {estimation} €"
    )
    if args.grafic:
        print(f"[BONUS] Generating grafic representation...")
        x_data,y_data = load_csv()
        if not x_data or not y_data:
            print(f"[ERROR] The data could not be retrieved from data.csv aborting bonus... ")
            sys.exit(1)


if __name__ == "__main__":
    main()