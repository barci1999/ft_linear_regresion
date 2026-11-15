import json
import os
from utils import print_box

FILE_PATH = "theta.json"


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
        exit(1)
    except EOFError:
        print("\nError: ctrl + d detected aborting")
        exit(1)
    except InvalidMielleageError as e:
        print(f"{e}")
        return(CheckImput())

def get_thetas():
    theta0,theta1 = 0.0,0.0
    if os.path.exists(FILE_PATH):
        try:
            print(f"{FILE_PATH}  detected")
            with open(FILE_PATH ,"r") as f:
                data_theta = json.load(f)
                raw_theta0 = data_theta.get("theta0") 
                raw_theta1 = data_theta.get("theta1")
                if raw_theta0 is None or raw_theta1 is None:
                    print(f"[ERROR] the keys theta0 or theta1 were not found in {FILE_PATH}.")
                    print(f"Using base values...")
                    return 0.0,0.0
                try:
                    theta0 = float(data_theta.get("theta0"))
                    theta1 = float(data_theta.get("theta1"))
                except (ValueError,TypeError) as e:
                    print(f"[ERROR] Invalid format in file {FILE_PATH}")
                    print(f"Values in File are:")
                    print(f"theta0 -> {raw_theta0}")
                    print(f"theta1 -> {raw_theta1}")
                    print(f"Using base values...")
                    return 0.0,0.0
        except PermissionError:
            print(f"[ERROR] The file ({FILE_PATH}) doesn't have the required permision,")
            print(f"Using base values...")
            return 0.0,0.0
        except json.JSONDecodeError:
            print(f"[ERROR] The file ({FILE_PATH}) doesn't have the correct format")
            print(f"Using base values...")
            return 0.0,0.0
        except Exception as e:
            print(f"[UNESPECTED ERROR] An error occurred while reading the file")
            print(f"Using base values...")
            return 0.0,0.0
    else:
        print(f"{FILE_PATH} no deteacted")
        print(f"Using base values...")
    return(theta0,theta1)
        
def get_estimation(theta0,theta1,milleage):

    estimation = theta0 + (theta1 * milleage)
    return(round(estimation,2))



def main():
    
    milleage = CheckImput()
    theta0,theta1 = get_thetas()
    print(f"theta0 = {theta0}")
    print(f"theta1 = {theta1}")
    print(f"{milleage}")
    estimation = get_estimation(theta0=theta0,theta1=theta1,milleage=milleage)
    print_box(
        "= RESULTS =",
        "---",
        f"milleage: {milleage} km",
        f"theta0: {theta0}",
        f"theta1: {theta1}",
        f"Estimation price: {estimation} €"
    )

if __name__ == "__main__":
    main()