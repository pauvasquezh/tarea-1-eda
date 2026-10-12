import csv
import statistics
import sys
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

sys.path.append(".")
from src.kdtree import construir_kdtree, vecino_exhaustivo, vecino_kdtree

DIMENSIONES = [2, 4, 8, 16, 32]
REPETICIONES = 7


def cargar_datos(d):
    X, y = load_digits(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    escalador = StandardScaler()
    escalador.fit(X_train)
    X_train = escalador.transform(X_train)
    X_test = escalador.transform(X_test)

    pca = PCA(n_components=d, svd_solver="full")
    pca.fit(X_train)
    X_train = pca.transform(X_train)
    X_test = pca.transform(X_test)

    return X_train.tolist(), X_test.tolist(), y_train.tolist(), y_test.tolist()


def tiempo_construccion(X_train):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        construir_kdtree(X_train)
        tiempos.append(time.perf_counter() - inicio)
    return statistics.median(tiempos)


def tiempo_exhaustiva(X_train, X_test):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for q in X_test:
            vecino_exhaustivo(X_train, q)
        tiempos.append(time.perf_counter() - inicio)
    return statistics.median(tiempos)


def tiempo_kdtree(raiz, X_test):
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for q in X_test:
            vecino_kdtree(raiz, q)
        tiempos.append(time.perf_counter() - inicio)
    return statistics.median(tiempos)


def experimento(d):
    X_train, X_test, y_train, y_test = cargar_datos(d)
    n_train = len(X_train)
    n_test = len(X_test)

    t_construccion = tiempo_construccion(X_train)
    raiz = construir_kdtree(X_train)
    t_exhaustiva = tiempo_exhaustiva(X_train, X_test)
    t_kdtree = tiempo_kdtree(raiz, X_test)

    pred_exhaustiva = []
    pred_kdtree = []
    visitados = []
    dist_exhaustiva = 0
    misma_distancia = 0
    mismo_indice = 0
    for q in X_test:
        i_exh, dist_exh, eval_exh = vecino_exhaustivo(X_train, q)
        i_kd, dist_kd, eval_kd = vecino_kdtree(raiz, q)
        pred_exhaustiva.append(y_train[i_exh])
        pred_kdtree.append(y_train[i_kd])
        visitados.append(eval_kd)
        dist_exhaustiva = dist_exhaustiva + eval_exh
        if dist_exh == dist_kd:
            misma_distancia = misma_distancia + 1
        if i_exh == i_kd:
            mismo_indice = mismo_indice + 1

    return {
        "d": d,
        "n_train": n_train,
        "n_test": n_test,
        "t_construccion": t_construccion,
        "t_exhaustiva_total": t_exhaustiva,
        "t_exhaustiva_consulta": t_exhaustiva / n_test,
        "t_kdtree_total": t_kdtree,
        "t_kdtree_consulta": t_kdtree / n_test,
        "speedup": t_exhaustiva / t_kdtree,
        "visitados_promedio": statistics.mean(visitados),
        "visitados_mediana": statistics.median(visitados),
        "fraccion_visitada": statistics.mean(visitados) / n_train,
        "dist_exhaustiva": dist_exhaustiva,
        "dist_kdtree": sum(visitados),
        "accuracy_exhaustiva": accuracy_score(y_test, pred_exhaustiva),
        "accuracy_kdtree": accuracy_score(y_test, pred_kdtree),
        "misma_distancia": misma_distancia / n_test,
        "mismo_indice": mismo_indice / n_test,
        "visitados": visitados,
    }

def coma(x, decimales):
    # Número con coma decimal, escrito para LaTeX.
    return f"{x:.{decimales}f}".replace(".", "{,}")


def miles(n):
    # Entero con separador de miles, escrito para LaTeX: 517\,320.
    return f"{n:,}".replace(",", "\\,")


def escribir_tabla(nombre, columnas, encabezado, filas):
    with open(f"informe/tablas/{nombre}.tex", "w", encoding="utf-8") as f:
        f.write("% Generado por scripts/act4_kdtree.py. No editar a mano.\n")
        f.write("\\begin{tabular}{" + columnas + "}\n")
        f.write("\\toprule\n")
        f.write(" & ".join(encabezado) + " \\\\\n")
        f.write("\\midrule\n")
        for fila in filas:
            f.write(" & ".join(fila) + " \\\\\n")
        f.write("\\bottomrule\n")
        f.write("\\end{tabular}\n")


def guardar_csv(resultados):
    columnas = [c for c in resultados[0] if c != "visitados"]
    with open("resultados/act4_kdtree.csv", "w", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(columnas)
        for r in resultados:
            escritor.writerow([r[c] for c in columnas])

    with open("resultados/act4_visitados_por_consulta.csv", "w", newline="") as f:
        escritor = csv.writer(f)
        escritor.writerow(["d", "consulta", "nodos_visitados"])
        for r in resultados:
            for i in range(len(r["visitados"])):
                escritor.writerow([r["d"], i, r["visitados"][i]])


def guardar_tablas(resultados):
    tiempos = []
    trabajo = []
    clasificacion = []
    for r in resultados:
        # La fila con d = 64 es la referencia sin reducción de dimensionalidad.
        d = str(r["d"]) if r["d"] != 64 else "64$^{*}$"
        tiempos.append([
            d,
            coma(1000 * r["t_construccion"], 1),
            coma(r["t_exhaustiva_total"], 3),
            coma(1000 * r["t_exhaustiva_consulta"], 3),
            coma(r["t_kdtree_total"], 3),
            coma(1000 * r["t_kdtree_consulta"], 3),
            coma(r["speedup"], 2),
        ])
        trabajo.append([
            d,
            coma(r["visitados_promedio"], 1),
            coma(r["visitados_mediana"], 0),
            coma(r["fraccion_visitada"], 3),
            coma(1 / r["fraccion_visitada"], 1),
            miles(r["dist_exhaustiva"]),
            miles(r["dist_kdtree"]),
        ])
        clasificacion.append([
            d,
            coma(r["accuracy_exhaustiva"], 4),
            coma(r["accuracy_kdtree"], 4),
            coma(100 * r["misma_distancia"], 1) + "\\,\\%",
            coma(100 * r["mismo_indice"], 1) + "\\,\\%",
        ])

    escribir_tabla("act4_tiempos", "crrrrrr",
                   ["$d$", "construcción (ms)", "exhaustiva total (s)",
                    "exhaustiva / consulta (ms)", "k-d tree total (s)",
                    "k-d tree / consulta (ms)", "speedup $S$"],
                   tiempos)
    escribir_tabla("act4_trabajo", "crrrrrr",
                   ["$d$", "visitados (promedio)", "visitados (mediana)",
                    "fracción visitada", "$1/\\text{fracción}$",
                    "distancias exhaustiva", "distancias k-d tree"],
                   trabajo)
    escribir_tabla("act4_clasificacion", "crrrr",
                   ["$d$", "accuracy exhaustiva", "accuracy k-d tree",
                    "misma distancia mínima", "mismo vecino"],
                   clasificacion)


def guardar_graficos(resultados):
    plt.rcParams["font.family"] = "serif"
    plt.rcParams["mathtext.fontset"] = "cm"

    # Los gráficos usan solo las dimensiones pedidas, sin la referencia d = 64.
    res = [r for r in resultados if r["d"] in DIMENSIONES]
    ds = [r["d"] for r in res]
    etiqueta_d = "dimensionalidad $d$ (componentes de PCA)"

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(ds, [1000 * r["t_exhaustiva_consulta"] for r in res], "o-",
            color="#dc2626", label="búsqueda exhaustiva")
    ax.plot(ds, [1000 * r["t_kdtree_consulta"] for r in res], "s-",
            color="#2563eb", label="k-d tree")
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(ds, [str(d) for d in ds])
    ax.set_xlabel(etiqueta_d)
    ax.set_ylabel("tiempo promedio por consulta (ms)")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.savefig("informe/figuras/act4_tiempo_consulta.pdf", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(ds, [r["speedup"] for r in res], "o-", color="#2563eb",
            label="speedup medido $S$")
    ax.plot(ds, [1 / r["fraccion_visitada"] for r in res], "s--", color="#6b7280",
            label="1 / fracción de nodos visitados")
    ax.axhline(1, color="black", linewidth=0.8)
    ax.set_xscale("log", base=2)
    ax.set_yscale("log")
    ax.set_xticks(ds, [str(d) for d in ds])
    ax.set_xlabel(etiqueta_d)
    ax.set_ylabel("speedup $S$")
    ax.grid(alpha=0.3)
    ax.legend()
    fig.savefig("informe/figuras/act4_speedup.pdf", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(ds, [r["fraccion_visitada"] for r in res], "o-", color="#2563eb")
    ax.set_xscale("log", base=2)
    ax.set_xticks(ds, [str(d) for d in ds])
    ax.set_ylim(0, 1)
    ax.set_xlabel(etiqueta_d)
    ax.set_ylabel("fracción promedio de nodos visitados")
    ax.grid(alpha=0.3)
    fig.savefig("informe/figuras/act4_fraccion_visitada.pdf", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(6, 3.8))
    ax.plot(ds, [r["accuracy_kdtree"] for r in res], "o-", color="#2563eb")
    ax.set_xscale("log", base=2)
    ax.set_xticks(ds, [str(d) for d in ds])
    ax.set_ylim(0, 1)
    ax.set_xlabel(etiqueta_d)
    ax.set_ylabel("accuracy 1-NN en prueba")
    ax.grid(alpha=0.3)
    fig.savefig("informe/figuras/act4_accuracy.pdf", bbox_inches="tight")

    fig, ax = plt.subplots(figsize=(6, 3.8))
    fracciones = []
    for r in res:
        fracciones.append([v / r["n_train"] for v in r["visitados"]])
    ax.boxplot(fracciones, tick_labels=[str(d) for d in ds],
               medianprops={"color": "#2563eb", "linewidth": 1.5},
               flierprops={"marker": ".", "markersize": 3, "alpha": 0.4})
    ax.set_ylim(0, 1.05)
    ax.set_xlabel(etiqueta_d)
    ax.set_ylabel("fracción de nodos visitados por consulta")
    ax.grid(alpha=0.3)
    fig.savefig("informe/figuras/act4_visitados_distribucion.pdf", bbox_inches="tight")


resultados = []
# Se agrega d = 64 (todas las componentes) como referencia sin reducción.
for d in DIMENSIONES + [64]:
    print("d =", d)
    resultados.append(experimento(d))

guardar_csv(resultados)
guardar_tablas(resultados)
guardar_graficos(resultados)
print("Listo: resultados/, informe/tablas/ e informe/figuras/ actualizados.")
