# ft_linear_regression

A from-scratch implementation of a **Simple Linear Regression** model in Python, designed to predict a car's price based on its mileage (`km`) using **Gradient Descent**, without relying on high-level Machine Learning libraries (such as `scikit-learn`)[cite: 6, 10, 11].


## Table of Contents

1. [What is this project for?](#what-is-this-project-for)
2. [Mathematical Background & Algorithm](#mathematical-background--algorithm)
   - [Hypothesis Function](#1-hypothesis-function)
   - [Cost Function (MSE)](#2-cost-function-mse)
   - [Gradient Descent](#3-gradient-descent)
   - [Z-Score Standardization & Denormalization](#4-z-score-standardization--denormalization)
3. [Project Architecture](#project-architecture)
4. [Requirements & Installation](#requirements--installation)
5. [Usage Guide](#usage-guide)
   - [Dataset Format (`data.csv`)](#dataset-format-datacsv)
   - [1. Training (`train.py`)](#1-training-trainpy)
   - [2. Prediction (`predict.py`)](#2-prediction-predictpy)
   - [3. Evaluation & Plotting (`bonus.py`)](#3-evaluation--plotting-bonuspy)
6. [Makefile Commands](#makefile-commands)

---

## What is this project for?

This project serves as a hands-on introduction to **Supervised Machine Learning**[cite: 11]. Its main goal is to solve a classic regression problem: **finding the optimal linear relationship between an independent feature ($x$, car mileage) and a dependent target variable ($y$, car price)** from a historical dataset (`data.csv`)[cite: 6, 9, 11].

From both a practical and educational standpoint, this project allows you to:
* **Model real-world trends:** Demonstrate how vehicle wear (higher mileage) translates into a linear depreciation of market value[cite: 11].
* **Understand training internals:** Manually implement the optimization loop, partial derivative calculations, simultaneous weight updates, and interactive hyperparameter tuning (`learning_rate` and `iterations`)[cite: 6, 11].
* **Handle numerical stability:** Apply data preprocessing techniques (Z-score standardization) to prevent numerical overflow and dramatically speed up algorithm convergence[cite: 6, 11].
* **Evaluate and visualize results:** Quantify model accuracy using Mean Absolute Error (MAE) and plot the fitted regression line against the real dataset[cite: 8, 11].

---

## Mathematical Background & Algorithm

### 1. Hypothesis Function

The model assumes that the estimated price of a car ($\hat{y}$) follows a straight line as a function of its mileage ($x$)[cite: 10, 11]:

$$\text{estimatePrice}(\text{mileage}) = \theta_0 + \theta_1 \cdot \text{mileage}$$

Where:
* **$\theta_0$ (Intercept / Bias):** Represents the theoretical base price of a vehicle with $0\text{ km}$[cite: 11].
* **$\theta_1$ (Slope / Weight):** Indicates how much the price changes per kilometer driven[cite: 11]. In this dataset it takes a negative value (around $-0.02145\text{ €/km}$), reflecting depreciation with use[cite: 11].

### 2. Cost Function (MSE)

To measure how well the regression line fits the $m$ real examples in the dataset, we use the **Mean Squared Error (MSE)**[cite: 11]:

$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)^2$$

The goal of training is to find the values of $\theta_0$ and $\theta_1$ that **minimize** $J(\theta_0, \theta_1)$[cite: 11].

### 3. Gradient Descent

Because the cost function is convex, it has a single global minimum[cite: 11]. **Gradient Descent** starts from $\theta_0 = 0.0$ and $\theta_1 = 0.0$ and takes iterative steps in the opposite direction of the gradient (the direction of steepest error increase)[cite: 6, 11].

At each iteration, average gradients are computed across the entire dataset (*Batch Gradient Descent*)[cite: 6, 11]:

$$\text{tmp}\theta_0 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)$$

$$\text{tmp}\theta_1 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right) \cdot x^{(i)}$$

Both parameters are then updated **simultaneously**[cite: 6, 11]:

$$\theta_0 := \theta_0 - \text{tmp}\theta_0$$

$$\theta_1 := \theta_1 - \text{tmp}\theta_1$$

Where $\alpha$ is the **learning rate**, controlling the step size of each update[cite: 6, 11].

### 4. Z-Score Standardization & Denormalization

In the raw dataset, mileage reaches hundreds of thousands ($20\,000$ – $240\,000\text{ km}$) and prices are in the thousands ($3\,000$ – $8\,500\text{ €}$)[cite: 11]. Running gradient descent directly on unscaled values causes the multiplication by $x^{(i)}$ to produce massive gradients, leading to `NaN` divergence unless an extremely tiny learning rate is used[cite: 11].

To prevent this, `train.py` applies **Z-score standardization** prior to training, rescaling both variables to have **mean $\mu = 0$** and **standard deviation $\sigma = 1$**[cite: 6, 11]:

$$x_{\text{norm}} = \frac{x - \mu_x}{\sigma_x}, \qquad y_{\text{norm}} = \frac{y - \mu_y}{\sigma_y}$$

Once the algorithm converges in normalized space ($\theta_{0,\text{norm}}, \theta_{1,\text{norm}}$), the weights are transformed back to real-world units (`km` and `€`) before saving them to `theta.json`, allowing `predict.py` to infer prices directly without reloading `data.csv`[cite: 6, 10, 11]:

$$\theta_{1,\text{real}} = \theta_{1,\text{norm}} \cdot \frac{\sigma_y}{\sigma_x}$$

$$\theta_{0,\text{real}} = \mu_y + \left(\sigma_y \cdot \theta_{0,\text{norm}}\right) - \left(\theta_{1,\text{real}} \cdot \mu_x\right)$$

---

## Project Architecture

```text
.
├── Makefile       # Automates virtual environment setup, dependencies, and execution
├── data.csv       # Historical dataset containing 'km' and 'price' columns
├── train.py       # Model training script using Z-score normalization & gradient descent
├── predict.py     # Main price inference/prediction CLI program
├── bonus.py       # Accuracy metric calculation (MAE) and regression visualization
├── utils.py       # Shared utilities (CSV parsing/validation, input checks, ASCII boxes)
└── theta.json     # Auto-generated file storing trained real-scale weights