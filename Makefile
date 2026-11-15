PYTHON = venv/bin/python
PIP = venv/bin/pip
PREDICT = predict.py
TRAIN = train.py

all:
	@echo "--- PROYECTO FT_LINEAR_REGRESSION ---"
	@echo "Comandos disponibles:"
	@echo "  make setup   - Crea el entorno virtual e instala matplotlib"
	@echo "  make train   - Entrena el modelo usando el venv"
	@echo "  make predict - Ejecuta la predicción normal usando el venv"
	@echo "  make bonus   - Ejecuta la predicción con el gráfico del bonus"
	@echo "  make clean   - Limpia __pycache__, theta.json y el entorno virtual"

# Regla para crear el entorno virtual e instalar dependencias automáticamente
venv:
	python3 -m venv venv
	$(PIP) install --upgrade pip
	$(PIP) install matplotlib

# setup: venv

# train: venv
# 	$(PYTHON) $(TRAIN)

# predict: venv
# 	$(PYTHON) $(PREDICT)

bonus: venv
	$(PYTHON) $(PREDICT) --grafic

clean:
	rm -rf __pycache__ .vscode theta.json venv
	@echo "Limpieza completada."

fclean: clean

re: clean all

.PHONY: all setup train predict bonus clean fclean re