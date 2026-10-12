def squared_distance(a, b):
    suma = 0.0
    for j in range(len(a)):
        diff = a[j] - b[j]
        suma = suma + diff * diff
    return suma


def construir(puntos, indices, depth):
    # Construye el árbol con los puntos cuyas posiciones están en `indices`.
    if len(indices) == 0:
        return None

    d = len(puntos[0])
    eje = depth % d

    # Ordenar las posiciones según la coordenada del eje y tomar la mediana.
    indices = sorted(indices, key=lambda i: puntos[i][eje])
    m = len(indices) // 2

    nodo = {
        "punto": puntos[indices[m]],
        "indice": indices[m],
        "eje": eje,
        "izquierdo": construir(puntos, indices[:m], depth + 1),
        "derecho": construir(puntos, indices[m + 1:], depth + 1),
    }
    return nodo


def construir_kdtree(puntos):
    return construir(puntos, list(range(len(puntos))), 0)


def vecino_exhaustivo(puntos, q):
    mejor_indice = -1
    mejor_dist = float("inf")
    for i in range(len(puntos)):
        dist = squared_distance(q, puntos[i])
        if dist < mejor_dist:
            mejor_dist = dist
            mejor_indice = i
    return mejor_indice, mejor_dist, len(puntos)


def buscar(nodo, q, mejor):
    # `mejor` guarda el mejor vecino encontrado y los nodos visitados.
    if nodo is None:
        return

    mejor["visitados"] = mejor["visitados"] + 1
    dist = squared_distance(q, nodo["punto"])
    if dist < mejor["dist"]:
        mejor["dist"] = dist
        mejor["indice"] = nodo["indice"]

    eje = nodo["eje"]
    delta = q[eje] - nodo["punto"][eje]
    if delta < 0:
        cerca = nodo["izquierdo"]
        lejos = nodo["derecho"]
    else:
        cerca = nodo["derecho"]
        lejos = nodo["izquierdo"]

    buscar(cerca, q, mejor)
    if delta * delta < mejor["dist"]:
        buscar(lejos, q, mejor)


def vecino_kdtree(raiz, q):
    mejor = {"indice": -1, "dist": float("inf"), "visitados": 0}
    buscar(raiz, q, mejor)
    return mejor["indice"], mejor["dist"], mejor["visitados"]
