"""
a_estrella.py
-------------
Algoritmo A* (A estrella) para encontrar el camino más corto de un peón
hasta su fila meta.

Lo usamos para dos cosas:
  1. Comprobar que un muro es legal (las reglas prohíben encerrar a un
     jugador: siempre tiene que existir algún camino hasta la meta).
  2. La función de evaluación del minimax: cuantos menos pasos le falten
     a un jugador para llegar, mejor está.

Cómo funciona A*:
  - Para cada casilla guarda g = pasos dados desde el inicio.
  - Estima lo que falta con una heurística h = filas que faltan hasta
    la meta (nunca sobreestima, porque cada paso avanza como mucho una fila).
  - Siempre expande primero la casilla con menor f = g + h.
"""

import heapq


def a_estrella(estado, inicio, fila_meta):
    """Devuelve la lista de casillas del camino más corto desde `inicio`
    hasta cualquier casilla de `fila_meta`, o None si no hay camino.
    El camino incluye la casilla de inicio."""

    def heuristica(casilla):
        return abs(casilla[0] - fila_meta)

    # Cola de prioridad con tuplas (f, g, casilla). heapq saca siempre la de menor f.
    abiertos = [(heuristica(inicio), 0, inicio)]
    coste = {inicio: 0}       # g: mejor número de pasos conocido hasta cada casilla
    padre = {inicio: None}    # de dónde venimos, para reconstruir el camino

    while abiertos:
        _, g, actual = heapq.heappop(abiertos)

        # ¿Hemos llegado a la fila meta? Reconstruimos el camino hacia atrás.
        if actual[0] == fila_meta:
            camino = []
            while actual is not None:
                camino.append(actual)
                actual = padre[actual]
            return camino[::-1]

        # Si ya encontramos un camino mejor a esta casilla, ignoramos esta entrada.
        if g > coste[actual]:
            continue

        for vecino in estado.vecinos(actual):
            nuevo_coste = g + 1
            if vecino not in coste or nuevo_coste < coste[vecino]:
                coste[vecino] = nuevo_coste
                padre[vecino] = actual
                heapq.heappush(abiertos, (nuevo_coste + heuristica(vecino), nuevo_coste, vecino))

    return None  # no hay ningún camino posible
