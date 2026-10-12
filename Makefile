PYTHON ?= python3

.PHONY: all instalar experimentos informe limpiar

## Reproduce todo: pruebas, experimentos (tablas y figuras) e informe PDF
all: experimentos informe

## Instala las dependencias de Python
instalar:
	$(PYTHON) -m pip install -r requirements.txt

## Regenera CSV, tablas LaTeX y figuras
experimentos:
	$(PYTHON) scripts/act2_log_vs_raiz.py
	$(PYTHON) scripts/act4_kdtree.py

## Compila el informe y deja una copia en la raíz como informe.pdf
informe:
	cd informe && latexmk main.tex
	cp informe/main.pdf informe.pdf

## Ejecuta las pruebas de correctitud
test:
	$(PYTHON) -m pytest -q

## Borra archivos auxiliares de LaTeX y cachés de Python
limpiar:
	cd informe && latexmk -C main.tex
	rm -rf informe/build .pytest_cache
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
