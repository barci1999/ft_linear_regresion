# ft_linear_regression

Implementación desde cero de un modelo de **Regresión Lineal Simple** en Python, diseñado para predecir el precio de un automóvil a partir de su kilometraje (`km`) utilizando el algoritmo de **Descenso de Gradiente (Gradient Descent)** sin depender de librerías de *Machine Learning* de alto nivel (como `scikit-learn`)[cite: 6, 10, 11].

---

## Tabla de Contenidos

1. [¿Para qué sirve este proyecto?](#para-qué-sirve-este-proyecto)
2. [Fundamento Matemático y Algoritmo](#fundamento-matemático-y-algoritmo)
   - [Función Hipótesis](#1-función-hipótesis)
   - [Función de Coste (MSE)](#2-función-de-coste-mse)
   - [Descenso de Gradiente](#3-descenso-de-gradiente)
   - [Normalización Z-Score y Desnormalización](#4-normalización-z-score-y-desnormalización)
3. [Arquitectura del Proyecto](#arquitectura-del-proyecto)
4. [Requisitos e Instalación](#requisitos-e-instalación)
5. [Guía de Uso](#guía-de-uso)
   - [Formato del Dataset (`data.csv`)](#formato-del-dataset-datacsv)
   - [1. Entrenamiento (`train.py`)](#1-entrenamiento-trainpy)
   - [2. Predicción (`predict.py`)](#2-predicción-predictpy)
   - [3. Evaluación y Gráfica (`bonus.py`)](#3-evaluación-y-gráfica-bonuspy)
6. [Comandos del Makefile](#comandos-del-makefile)

---

## ¿Para qué sirve este proyecto?

Este proyecto constituye una introducción práctica al **Aprendizaje Automático Supervisado (Supervised Machine Learning)**. Su objetivo principal es resolver un problema clásico de regresión: **encontrar la relación lineal óptima entre una variable independiente o característica ($x$, el kilometraje) y una variable dependiente u objetivo ($y$, el precio)** a partir de un conjunto de datos históricos (`data.csv`)[cite: 6, 9, 11].

A nivel práctico y educativo, el proyecto permite:
* **Modelar tendencias reales:** Demostrar cómo el desgaste de un vehículo (mayor kilometraje) se traduce en una depreciación lineal de su valor de mercado.
* **Comprender el entrenamiento desde dentro:** Implementar manualmente el bucle de optimización, el cálculo de derivadas parciales, la actualización simultánea de pesos y el control interactivo de hiperparámetros (`learning_rate` e `iterations`)[cite: 6, 11].
* **Resolver problemas numéricos reales:** Aplicar técnicas de preprocesamiento de datos (estandarización Z-score) para evitar desbordamientos numéricos (*overflow*) y acelerar drásticamente la convergencia del algoritmo[cite: 6, 11].
* **Evaluar y visualizar resultados:** Cuantificar la precisión del modelo mediante el Error Absoluto Medio (MAE) y representar gráficamente el ajuste de la recta frente a los datos reales[cite: 8, 11].

---

## Fundamento Matemático y Algoritmo

### 1. Función Hipótesis

El modelo asume que el precio estimado de un coche ($\hat{y}$) sigue la ecuación de una recta en función de su kilometraje ($x$)[cite: 10, 11]:

$$\text{estimatePrice}(\text{mileage}) = \theta_0 + \theta_1 \cdot \text{mileage}$$

Donde:
* **$\theta_0$ (Intercepto o sesgo):** Representa el precio base teórico de un vehículo con $0\text{ km}$[cite: 11].
* **$\theta_1$ (Pendiente o peso):** Indica cuánto varía el precio por cada kilómetro recorrido[cite: 11]. En este problema toma un valor negativo (aproximadamente $-0.02145\text{ €/km}$), reflejando la pérdida de valor por uso[cite: 11].

### 2. Función de Coste (MSE)

Para medir qué tan bien se ajusta nuestra recta a los $m$ ejemplos reales del dataset, se utiliza el **Error Cuadrático Medio (Mean Squared Error)**[cite: 11]:

$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)^2$$

El objetivo del entrenamiento es encontrar los valores de $\theta_0$ y $\theta_1$ que **minimicen** $J(\theta_0, \theta_1)$[cite: 11].

### 3. Descenso de Gradiente

Al tratarse de una función convexa, existe un único mínimo global[cite: 11]. El **Descenso de Gradiente** parte de $\theta_0 = 0.0$ y $\theta_1 = 0.0$ y da pasos iterativos en la dirección opuesta al gradiente (la pendiente de mayor crecimiento del error)[cite: 6, 11].

En cada iteración, se calculan los gradientes promedio sobre todo el dataset (*Batch Gradient Descent*)[cite: 6, 11]:

$$\text{tmp}\theta_0 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)$$

$$\text{tmp}\theta_1 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right) \cdot x^{(i)}$$

Y ambos parámetros se actualizan **simultáneamente**[cite: 6, 11]:

$$\theta_0 := \theta_0 - \text{tmp}\theta_0$$

$$\theta_1 := \theta_1 - \text{tmp}\theta_1$$

Donde $\alpha$ es la **tasa de aprendizaje (`learning_rate`)**, que controla el tamaño de cada paso[cite: 6, 11].

### 4. Normalización Z-Score y Desnormalización

En el dataset real, los kilometrajes alcanzan cientos de miles ($20\,000$ – $240\,000\text{ km}$) y los precios miles de euros ($3\,000$ – $8\,500\text{ €}$)[cite: 11]. Si aplicáramos el descenso de gradiente directamente sobre estas magnitudes, la multiplicación por $x^{(i)}$ generaría gradientes gigantescos que harían divergir el algoritmo hacia `NaN` o requerirían tasas de aprendizaje minúsculas[cite: 11].

Para solucionarlo, `train.py` aplica una **estandarización Z-score** antes de entrenar, transformando ambas variables para que tengan **media $\mu = 0$** y **desviación estándar $\sigma = 1$**[cite: 6, 11]:

$$x_{\text{norm}} = \frac{x - \mu_x}{\sigma_x}, \qquad y_{\text{norm}} = \frac{y - \mu_y}{\sigma_y}$$

Una vez que el algoritmo converge en el espacio normalizado ($\theta_{0,\text{norm}}, \theta_{1,\text{norm}}$), los pesos se transforman de vuelta a la escala real (`km` y `€`) antes de guardarse en `theta.json`, permitiendo que `predict.py` opere directamente con valores reales sin necesidad de volver a leer `data.csv`[cite: 6, 10, 11]:

$$\theta_{1,\text{real}} = \theta_{1,\text{norm}} \cdot \frac{\sigma_y}{\sigma_x}$$

$$\theta_{0,\text{real}} = \mu_y + \left(\sigma_y \cdot \theta_{0,\text{norm}}\right) - \left(\theta_{1,\text{real}} \cdot \mu_x\right)$$

---

## Arquitectura del Proyecto

```text
.
├── Makefile       # Automatización de entorno virtual, dependencias y ejecución
├── data.csv       # Dataset histórico con columnas 'km' y 'price'
├── train.py       # Entrenamiento del modelo con normalización y descenso de gradiente
├── predict.py     # Programa principal de inferencia/predicción de precios
├── bonus.py       # Cálculo de precisión (MAE) y visualización gráfica de la regresión
├── utils.py       # Utilidades compartidas (lectura/validación CSV, inputs, formato en caja)
└── theta.json     # Archivo generado automáticamente con los pesos entrenados