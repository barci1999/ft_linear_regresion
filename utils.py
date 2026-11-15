import argparse
import sys

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
        return(CheckImput())

def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grafic","-g",
    action="store_true",
    help="Display the graph with the scatter plot and the regression line (Bonus).")
    return(parser.parse_args())
    