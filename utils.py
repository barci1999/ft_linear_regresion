import argparse
import sys
import csv

THETA_FILEPATH = "theta.json"
CSV_FILEPATH = "data.csv"

def print_box(*lines):
    str_lines = [str(line) for line in lines]
    text_lines = [l for l in str_lines if l != "---"]
    max_len = max(len(line) for line in text_lines) if text_lines else 0
    
    border = "+" + "-" * (max_len + 2) + "+"
    divider = "|" + "-" * (max_len + 2) + "|"
    
    print(border)
    for line in str_lines:
        if line == "---":
            print(divider)
        else:
            print(f"| {line.ljust(max_len)} |")
    print(border)


class InvalidMielleageError(Exception):
    """Excepcion personalizada"""
    pass


def CheckImput():
    try:
        data = input("insert values -> ")
        if not data.strip():
            raise InvalidMielleageError(f"Error: the input cant be empty '{data}'")
        try:
            milleage = float(data)
        except ValueError:
            raise InvalidMielleageError(f"Error: the input must be a valid number '{data}'")
        if milleage <= 0:
            raise InvalidMielleageError(f"Error: the input must be a positive number '{data}'")
        return milleage
    except KeyboardInterrupt:
        print("\nError: ctrl + c detected aborting")
        sys.exit(1)
    except EOFError:
        print("\nError: ctrl + d detected aborting")
        sys.exit(1)
    except InvalidMielleageError as e:
        print(f"{e}")
        return CheckImput()

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grafic","-g",
    action="store_true",
    help="Display the graph with the scatter plot and the regression line (Bonus).")
    return parser.parse_args()
    
def load_csv():
    x_data = []
    y_data = []
    try:
        with open(CSV_FILEPATH, mode='r', encoding='utf-8') as file:
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