"""
minimax.py
----------
La inteligencia artificial: Minimax con poda alfa-beta.

Minimax:
  - La IA (MAX) quiere que la puntuación sea lo más ALTA posible.
  - El humano (MIN) quiere que sea lo más BAJA posible.
  - Se prueban las jugadas varios turnos hacia delante y se elige la que da
    mejor resultado suponiendo que el rival también juega lo mejor posible.

Poda alfa-beta:
  - alfa = lo mejor que MAX ya tiene asegurado en otra rama.
  - beta = lo mejor que MIN ya tiene asegurado en otra rama.
  - Si alfa >= beta, el rival nunca dejaría llegar a esta rama, así que
    dejamos de explorarla. Da el mismo resultado que sin poda, pero mucho más rápido.
"""

import math

from tablero import (HUMANO, IA, aplicar, camino, distancia, ganador,
                     movimientos_peon, muro_valido, muros_que_bloquean)

PROFUNDIDAD = 4  # turnos que mira hacia delante (mejor par: la IA y el humano mueven lo mismo)
VICTORIA = 1000  # puntuación de una partida ganada
PESO_MUROS = 5   # cuánto vale guardar un muro (un paso de ventaja vale 10)


def evaluar(estado, profundidad):
    """Puntuación del estado para la IA: positiva = va ganando la IA."""
    quien_gana = ganador(estado)
    # Sumamos la profundidad que queda para preferir ganar cuanto antes (y perder lo más tarde posible).
    if quien_gana == IA:
        return VICTORIA + profundidad
    if quien_gana == HUMANO:
        return -VICTORIA - profundidad

    # Lo que importa: cuántos pasos le faltan a cada uno (calculado con A*)...
    ventaja_pasos = distancia(estado, HUMANO) - distancia(estado, IA)
    # ...y cuántos muros le quedan a cada uno para el resto de la partida.
    ventaja_muros = estado['muros_restantes'][IA] - estado['muros_restantes'][HUMANO]
    return 10 * ventaja_pasos + PESO_MUROS * ventaja_muros


def jugadas_a_probar(estado):
    """Las jugadas que el minimax va a probar (no todas: solo las que tienen sentido).
    Usa yield: cada jugada se calcula justo cuando el minimax la pide, así que si
    la poda corta la búsqueda, las que faltaban ni se llegan a comprobar."""
    yo = estado['turno']

    # 1) Mover el peón, pero solo a casillas que lo acercan a la meta (si ninguna acerca, todas).
    #    Así la IA no se queda yendo y viniendo entre dos casillas por miedo a un muro.
    movimientos = [('mover', f, c) for f, c in movimientos_peon(estado, yo)]
    ahora = distancia(estado, yo)
    yield from [j for j in movimientos if distancia(aplicar(estado, j), yo) < ahora] or movimientos

    # 2) Poner un muro, pero solo los que cortan el camino más corto del rival.
    #    Hay hasta ~130 muros posibles; el resto no le retrasa y solo haría la búsqueda más lenta.
    if estado['muros_restantes'][yo] > 0:
        ruta = camino(estado, 1 - yo)
        cortan = {muro for a, b in zip(ruta, ruta[1:]) for muro in muros_que_bloquean(a, b)}
        for muro in sorted(cortan):
            if muro_valido(estado, muro):
                yield muro


def minimax(estado, profundidad, alfa, beta):
    """Devuelve (puntuación, mejor jugada) para el jugador que tiene el turno."""
    if profundidad == 0 or ganador(estado) is not None:
        return evaluar(estado, profundidad), None

    mejor_jugada = None

    if estado['turno'] == IA:
        # MAX: buscamos la puntuación más alta.
        mejor = -math.inf
        for jugada in jugadas_a_probar(estado):
            puntuacion, _ = minimax(aplicar(estado, jugada), profundidad - 1, alfa, beta)
            if puntuacion > mejor:
                mejor, mejor_jugada = puntuacion, jugada
            alfa = max(alfa, mejor)
            if alfa >= beta:
                break  # poda: MIN nunca dejaría llegar aquí
    else:
        # MIN: buscamos la puntuación más baja.
        mejor = math.inf
        for jugada in jugadas_a_probar(estado):
            puntuacion, _ = minimax(aplicar(estado, jugada), profundidad - 1, alfa, beta)
            if puntuacion < mejor:
                mejor, mejor_jugada = puntuacion, jugada
            beta = min(beta, mejor)
            if alfa >= beta:
                break  # poda: MAX nunca dejaría llegar aquí

    return mejor, mejor_jugada


def mejor_movimiento(estado, profundidad=PROFUNDIDAD):
    """La jugada que elige la IA."""
    return minimax(estado, profundidad, -math.inf, math.inf)[1]
