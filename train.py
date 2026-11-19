import sys
import argparse
import json
import numpy as np
from utils import load_csv,THETA_FILEPATH
from predict import get_thetas,get_estimation

DEFAULT_LEARNING_RATE = 0.1
DEFAULT_ITERACTIONS = 1000

def get_error(prediction,price):
    return (prediction - price)

def normalice_values(kms_data,price_data):
    res_kms,res_price = [],[]
    if not kms_data or not price_data:
        print(f"[ERROR] The data could not be retrieved from data.csv aborting...")
        sys.exit(1)
    mean_kms = np.mean(kms_data)
    mean_price = np.mean(price_data)
    std_kms = np.std(kms_data)
    std_price = np.std(price_data)
    if std_price == 0:
        print(f"[ERROR] Standar desviation of price is 0 that mean all the price in csv are the same...")
        sys.exit(1)
    if std_kms == 0:
        print(f"[ERROR] Standar desviation of kms is 0 that mean all the kms in csv are the same...")
        sys.exit(1)
    for t in kms_data:
        res_kms.append((t - mean_kms) / std_kms)
    for t in price_data:
        res_price.append((t - mean_price) / std_price)
    return res_kms,res_price,mean_kms,mean_price,std_kms,std_price

def save_theta_file(theta0,theta1,mean_kms,mean_price,std_kms,std_price):
    res_theta1 = theta1 * (std_price / std_kms)
    res_theta0 = mean_price + (std_price * theta0) - (res_theta1 * mean_kms)
    payload = {
        "theta0": float(res_theta0),
        "theta1": float(res_theta1),
    }

    try:
        with open(THETA_FILEPATH, "w", encoding="utf-8") as file:
            json.dump(payload, file, indent=4)
    except OSError as exc:
        print(f"[ERROR] Could not write {filepath}: {exc}")
        sys.exit(1)

def prompt_param(label, default_value, cast_type):
    raw = input(f"{label} [{default_value}]: ").strip()
    if raw == "":
        return default_value

    try:
        value = cast_type(raw)
    except ValueError:
        print(f"[ERROR] Invalid value '{raw}' for {label}.")
        sys.exit(1)

    if value <= 0:
        print(f"[ERROR] {label} must be greater than 0.")
        sys.exit(1)

    return value

def main():
    learning_rate = prompt_param("Learning rate", DEFAULT_LEARNING_RATE, float)
    iterations = prompt_param("iteration", DEFAULT_ITERACTIONS, int)
    theta0,theta1 = 0.0,0.0
    raw_kms,raw_price = load_csv()
    norm_kms,norm_price,mean_kms,mean_price,std_kms,std_price= normalice_values(raw_kms,raw_price)

    for _ in range(iterations):
        new_theta0,new_theta1 = 0.0,0.0
        for kms,price in zip(norm_kms,norm_price):
            estimation = get_estimation(theta0=theta0,theta1=theta1,milleage=kms)
            error = get_error(prediction=estimation,price=price)
            new_theta0 += error
            new_theta1 += error * kms
        new_theta0 /= len(norm_kms)
        new_theta1 /= len(norm_kms)
        theta0 -= learning_rate * new_theta0
        theta1 -= learning_rate * new_theta1
    save_theta_file(theta0=theta0,theta1=theta1,mean_kms=mean_kms,mean_price=mean_price,std_kms=std_kms,std_price=std_price)

    
    

if __name__ == "__main__":
    main()