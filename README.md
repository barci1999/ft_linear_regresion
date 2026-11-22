# ft_linear_regression

Implementación desde cero de un modelo de **Regresión Lineal Simple** en Python, diseñado para predecir el precio de un automóvil a partir de su kilometraje (`km`) utilizando el algoritmo de **Descenso de Gradiente (Gradient Descent)** sin depender de librerías de *Machine Learning* de alto nivel (como `scikit-learn`).

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

Este proyecto constituye una introducción práctica al **Aprendizaje Automático Supervisado (Supervised Machine Learning)**. Su objetivo principal es resolver un problema clásico de regresión: **encontrar la relación lineal óptima entre una variable independiente o característica ($x$, el kilometraje) y una variable dependiente u objetivo ($y$, el precio)** a partir de un conjunto de datos históricos (`data.csv`).

A nivel práctico y educativo, el proyecto permite:
* **Modelar tendencias reales:** Demostrar cómo el desgaste de un vehículo (mayor kilometraje) se traduce en una depreciación lineal de su valor de mercado.
* **Comprender el entrenamiento desde dentro:** Implementar manualmente el bucle de optimización, el cálculo de derivadas parciales, la actualización simultánea de pesos y el control de hiperparámetros (`learning_rate` e `iterations`).
* **Resolver problemas numéricos reales:** Aplicar técnicas de preprocesamiento de datos (estandarización Z-score) para evitar desbordamientos numéricos (*overflow*) y acelerar drásticamente la convergencia del algoritmo.
* **Evaluar y visualizar resultados:** Cuantificar la precisión del modelo mediante métricas de error (MAE) y representar gráficamente el ajuste de la recta frente a los datos reales.

---

## Fundamento Matemático y Algoritmo

### 1. Función Hipótesis

El modelo asume que el precio estimado de un coche ($\hat{y}$) sigue la ecuación de una recta en función de su kilometraje ($x$):

$$\text{estimatePrice}(\text{mileage}) = \theta_0 + \theta_1 \cdot \text{mileage}$$

Donde:
* **$\theta_0$ (Intercepto o sesgo):** Representa el precio base teórico de un vehículo con $0\text{ km}$.
* **$\theta_1$ (Pendiente o peso):** Indica cuánto varía el precio por cada kilómetro recorrido. En este problema toma un valor negativo (aproximadamente $-0.02145\text{ €/km}$), reflejando la pérdida de valor por uso.

### 2. Función de Coste (MSE)

Para medir qué tan bien se ajusta nuestra recta a los $m$ ejemplos reales del dataset, se utiliza el **Error Cuadrático Medio (Mean Squared Error)**:

$$J(\theta_0, \theta_1) = \frac{1}{2m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)^2$$

El objetivo del entrenamiento es encontrar los valores de $\theta_0$ y $\theta_1$ que **minimicen** $J(\theta_0, \theta_1)$.

### 3. Descenso de Gradiente

Al tratarse de una función convexa, existe un único mínimo global. El **Descenso de Gradiente** parte de $\theta_0 = 0$ y $\theta_1 = 0$ y da pasos iterativos en la dirección opuesta al gradiente (la pendiente de mayor crecimiento del error).

En cada iteración, se calculan los gradientes promedio sobre todo el dataset (*Batch Gradient Descent*):

$$\text{tmp}\theta_0 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right)$$

$$\text{tmp}\theta_1 = \alpha \cdot \frac{1}{m} \sum_{i=0}^{m-1} \left( \text{estimatePrice}(x^{(i)}) - y^{(i)} \right) \cdot x^{(i)}$$

Y ambos parámetros se actualizan **simultáneamente**:

$$\theta_0 := \theta_0 - \text{tmp}\theta_0$$

$$\theta_1 := \theta_1 - \text{tmp}\theta_1$$

Donde $\alpha$ es la **tasa de aprendizaje (`learning_rate`)**, que controla el tamaño de cada paso.

### 4. Normalización Z-Score y Desnormalización

En el dataset real, los kilometrajes alcanzan cientos de miles ($20\,000$ – $240\,000\text{ km}$) y los precios miles de euros ($3\,000$ – $8\,500\text{ €}$). Si aplicáramos el descenso de gradiente directamente sobre estas magnitudes, la multiplicación por $x^{(i)}$ generaría gradientes gigantescos que harían divergir el algoritmo hacia `NaN` o requerirían tasas de aprendizaje minúsculas.

Para solucionarlo, `train.py` aplica una **estandarización Z-score** antes de entrenar, transformando ambas variables para que tengan **media $\mu = 0$** y **desviación estándar $\sigma = 1$**:

$$x_{\text{norm}} = \frac{x - \mu_x}{\sigma_x}, \qquad y_{\text{norm}} = \frac{y - \mu_y}{\sigma_y}$$

Una vez que el algoritmo converge en el espacio normalizado ($\theta_{0,\text{norm}}, \theta_{1,\text{norm}}$), los pesos se transforman de vuelta a la escala real (`km` y `€`) antes de guardarse en `theta.json`, permitiendo que `predict.py` opere directamente con valores reales sin necesidad de volver a leer `data.csv`:

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
```

### Detalle de cada módulo

* **`train.py`**:
  * Solicita interactivamente por terminal los hiperparámetros `Learning rate` (por defecto `0.1`) e `iteration` (por defecto `1000`), validando que sean valores numéricos estrictamente positivos.
  * Carga `data.csv`, verifica que no esté vacío y comprueba que la desviación estándar de `km` y `price` sea distinta de cero para evitar divisiones por cero.
  * Inicializa $\theta_0 = 0.0$ y $\theta_1 = 0.0$ en espacio normalizado, ejecuta el bucle de descenso de gradiente, desnormaliza los parámetros resultantes y los persiste en `theta.json`.
* **`predict.py`**:
  * Lee `theta0` y `theta1` desde `theta.json`. Si el archivo no existe o presenta errores de formato/permisos, utiliza `0.0` y `0.0` de forma segura.
  * Valida la entrada del usuario (rechazando entradas vacías, texto no numérico, valores $\le 0$ e interrupciones `Ctrl+C` / `Ctrl+D`).
  * Imprime los resultados formateados en una tabla ASCII en terminal.
* **`bonus.py`**:
  * Evalúa la precisión del modelo calculando el **Error Absoluto Medio (MAE)** sobre todos los registros de `data.csv`:
    $$\text{MAE} = \frac{1}{m} \sum_{i=0}^{m-1} \left| y^{(i)} - \hat{y}^{(i)} \right|$$
  * Genera un gráfico interactivo con `matplotlib` superponiendo la nube de puntos reales (*scatter plot*) y la recta de regresión calculada.
* **`utils.py`**:
  * Centraliza constantes (`THETA_FILEPATH`, `CSV_FILEPATH`), validación estricta de cabeceras y tipos del CSV, manejo de excepciones personalizadas (`InvalidMielleageError`) y renderizado visual de cajas en consola (`print_box`).

---

## Requisitos e Instalación

* **Python 3.8+**
* **Dependencias:** `numpy` (cálculos estadísticos de media y desviación estándar en `train.py`) y `matplotlib` (visualización gráfica en `bonus.py`).

Para preparar el entorno virtual aislado (`venv/`) e instalar las dependencias:

```bash
make venv
venv/bin/pip install numpy
```

---

## Guía de Uso

### Formato del Dataset (`data.csv`)

El archivo `data.csv` debe contener exactamente las cabeceras `km,price` seguidas de filas numéricas válidas:

```csv
km,price
240000,3650
139800,3800
150500,4400
...
```

### 1. Entrenamiento (`train.py`)

Inicia el entrenamiento ejecutando:

```bash
make train
```

El programa te pedirá los hiperparámetros por consola (pulsa `Enter` para aceptar los valores base entre corchetes):

```text
venv/bin/python train.py
Learning rate [0.1]: 0.01
iteration [1000]: 5000
```

Al finalizar, se creará o actualizará `theta.json` con los pesos ajustados en escala real:

```json
{
    "theta0": 8498.715264453658,
    "theta1": -0.021450270933144354
}
```

### 2. Predicción (`predict.py`)

Una vez entrenado el modelo (o incluso antes de entrenarlo, partiendo de $\theta_0 = 0, \theta_1 = 0$), ejecuta:

```bash
make predict
```

Introduce el kilometraje del coche que deseas valorar:

```text
venv/bin/python predict.py
insert values -> 100000
theta.json detected
+-------------------------------+
| = RESULTS =                   |
|-------------------------------|
| milleage: 100000.0 km         |
| theta0: 8498.715264453658     |
| theta1: -0.021450270933144354 |
| Estimation price: 6353.69 €   |
+-------------------------------+
```

### 3. Evaluación y Gráfica (`bonus.py`)

Para comprobar el error medio del modelo sobre los datos reales y visualizar la recta de regresión:

```bash
make bonus
```

Salida en terminal y apertura de ventana gráfica:

```text
venv/bin/python bonus.py
theta.json detected
Error absoluto medio (MAE): 557.83 €
```

---

## Comandos del Makefile

| Comando | Descripción |
| :--- | :--- |
| `make` / `make all` | Muestra la ayuda y los comandos disponibles en el proyecto. |
| `make venv` | Crea el entorno virtual `venv` e instala dependencias base. |
| `make train` | Ejecuta `train.py` dentro del entorno virtual para entrenar el modelo. |
| `make predict` | Ejecuta `predict.py` dentro del entorno virtual para estimar precios. |
| `make bonus` | Ejecuta `bonus.py` para mostrar el MAE y el gráfico de dispersión + recta. |
| `make clean` / `fclean` | Elimina `__pycache__`, `.vscode`, `theta.json` y el entorno `venv`. |
| `make re` | Limpia todos los archivos generados y vuelve a mostrar el menú principal. |