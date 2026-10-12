# Tarea 1: Análisis asintótico y Dividir para conquistar

Tarea 1 de **Algoritmos y Estructuras de Datos**, Doctorado en Inteligencia Artificial.
Contiene el desarrollo formal de ejercicios de análisis asintótico de algoritmos
iterativos y recursivos, algoritmos Dividir para Conquistar, y una implementación de un
**k-d tree** para búsqueda de vecinos cercanos.

- **Informe:** [`informe.pdf`](informe.pdf)
- **Integrantes:** Paula Vásquez-Henríquez y Guillermo Zieballe
- **Profesora:** Cecilia Hernández

## Estructura del repositorio

```
.
├── informe.pdf              # Informe final (compilado)
├── informe/                 # Fuente LaTeX del informe
│   ├── main.tex             #   documento principal
│   ├── preambulo.tex        #   paquetes y macros
│   ├── portada.tex
│   ├── secciones/           #   una sección por actividad 
│   ├── figuras/             #   logos/ de la portada y figuras generadas por scripts/
│   └── tablas/              #   tablas generadas por scripts/ 
├── src/                     
│   └── kdtree.py            #   k-d tree, búsqueda exhaustiva y squared_distance (Actividad 4)
├── scripts/                 # Scripts que generan tablas, figuras y datos
│   ├── act2_log_vs_raiz.py  #   gráfico de log2(n) y sqrt(n) de la Actividad 2.2
│   └── act4_kdtree.py       #   experimentos de la Actividad 4
├── resultados/              # Datos crudos de los experimentos (CSV)
└── requirements.txt         # Dependencias de Python con versiones fijas
```

## Dependencias

- **Python 3.12** con los paquetes de [`requirements.txt`](requirements.txt).
- **LaTeX** (TeX Live o MacTeX) con `latexmk`, solo para recompilar el informe.

## Reproducir los resultados

```bash
# 1. Crear un entorno virtual e instalar dependencias
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# 2. Regenerar tablas, figuras y datos (entre 1 y 2 minutos)
python scripts/act2_log_vs_raiz.py
python scripts/act4_kdtree.py

# 3. Compilar el informe
cd informe && latexmk main.tex
```

Todos los comandos se ejecutan desde la raíz del repositorio.
