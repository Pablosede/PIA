from math import inf
from a_star import AStar
from Grafo2P3_2 import crear_grafo


# Ejercicio 4
def reset_graph(g):
    for nodo in g.nodes:
        nodo.parent = None
        nodo.heuristic_value = -1
        nodo.distance_from_start = inf


# Ejercicio 5
def ruta(origen, destino, grafo, mostrar_pasos=False):
    reset_graph(grafo)  # limpiar la búsqueda anterior antes de empezar
    astar = AStar(grafo, origen, destino, mostrar_pasos)
    resultado = astar.search()

    if resultado is None:
        print(f"No hay ruta entre {origen} y {destino}")
    else:
        camino, coste = resultado
        print(f"Ruta de {origen} a {destino}: {' -> '.join(camino)} (coste {coste})")


if __name__ == "__main__":
    grafo = crear_grafo()

    # Ejercicio 6
    print("Ejercicio 6")
    ruta("A", "B", grafo)   # a)
    ruta("A", "G", grafo)   # b)
    ruta("A", "H", grafo)   # c)
    ruta("G", "C", grafo)   # d)

    # Ejercicios 7 y 8: búsqueda de A a E mostrando cada iteración
    print("\nEjercicio 8")
    ruta("A", "E", grafo, mostrar_pasos=True)
