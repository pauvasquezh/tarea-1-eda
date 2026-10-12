# Actividad 1: algoritmos A y B.
# En vez de ejecutar Operation(), cada función cuenta cuántas veces se ejecutaría.
# Junto a cada algoritmo están las fórmulas del informe, para compararlas con el conteo.


# ---- Algoritmo A ------------------------------------------------------------


def algoritmo_a(n):
    ejecuciones = 0
    for i in range(1, n + 1):
        j = i
        while j <= n:
            ejecuciones = ejecuciones + 1  # Operation()
            j = 2 * j
    return ejecuciones


def log2_piso(x):
    # floor(log2(x)) para un entero x >= 1, contando cuántas veces se divide por 2.
    k = 0
    while x >= 2:
        x = x // 2
        k = k + 1
    return k


def vueltas_para_i(n, i):
    # Parte (a): floor(log2(n/i)) + 1.
    return log2_piso(n // i) + 1


def suma_por_i(n):
    # Parte (b): suma de las vueltas para i = 1, ..., n.
    total = 0
    for i in range(1, n + 1):
        total = total + vueltas_para_i(n, i)
    return total


def valores_que_llegan(n, k):
    # Parte (c): cuántos valores de i llegan a la iteración k, floor(n / 2^(k-1)).
    return n // 2 ** (k - 1)


def suma_por_iteracion(n):
    # Parte (c): suma de floor(n / 2^m) para m = 0, ..., floor(log2 n).
    total = 0
    for m in range(log2_piso(n) + 1):
        total = total + n // 2**m
    return total


# ---- Algoritmo B ------------------------------------------------------------


def algoritmo_b(n):
    ejecuciones = 0
    m = n
    while m >= 1:
        for i in range(1, m + 1):
            j = 1
            while j <= m:
                ejecuciones = ejecuciones + 1  # Operation()
                j = 2 * j
        m = m // 2
    return ejecuciones


def trabajo_para_m(m):
    # Parte (a): m * (floor(log2 m) + 1).
    return m * (log2_piso(m) + 1)


def valores_de_m(n):
    # Parte (b): los valores que toma m, floor(n / 2^t) para t = 0, ..., floor(log2 n).
    valores = []
    for t in range(log2_piso(n) + 1):
        valores.append(n // 2**t)
    return valores


def suma_por_m(n):
    # Parte (b): suma del trabajo para cada valor de m.
    total = 0
    for m in valores_de_m(n):
        total = total + trabajo_para_m(m)
    return total
