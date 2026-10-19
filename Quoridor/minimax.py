"""
minimax.py
----------
La inteligencia artificial: Minimax con poda alfa-beta.

Idea del minimax:
  - La IA (MAX) quiere que la puntuación sea lo más ALTA posible.
  - El humano (MIN) quiere que sea lo más BAJA posible.
  - Se exploran las jugadas unos cuantos turnos hacia delante y se elige
    la que da mejor resultado suponiendo que el rival también juega bien.

Poda alfa-beta:
  - alfa = lo mejor que MAX ya tiene asegurado en otra rama.
  - beta = lo mejor que MIN ya tiene asegurado en otra rama.
  - Si en una rama alfa >= beta, el rival nunca dejaría llegar a ella,
    así que dejamos de explorarla (la "podamos"). El resultado es el
    mismo que sin poda, pero mucho más rápido.

Como en Quoridor hay hasta ~130 muros posibles por turno, solo probamos
los muros que cortan el camino más corto del rival (calculado con A*).
Son los únicos que de verdad le retrasan, y así el árbol es manejable.
"""

import math

from tablero import IA, HUMANO

# Turnos que mira hacia delante. Mejor un número par, para que la IA y el humano
# muevan las mismas veces en la simulación. Con 4 juega mejor, pero puede tardar unos segundos.
PROFUNDIDAD = 2
VICTORIA = 1000  # puntuación de una partida ganada


def evaluar(estado, profundidad):
    """Puntuación del estado desde el punto de vista de la IA (más alto = mejor para la IA)."""
    ganador = estado.ganador()
    # Sumamos la profundidad que queda para preferir ganar cuanto antes (y perder cuanto más tarde).
    if ganador == IA:
        return VICTORIA + profundidad
    if ganador == HUMANO:
        return -VICTORIA - profundidad

    # Lo importante: cuántos pasos le faltan a cada uno (con A*).
    ventaja_camino = estado.distancia(HUMANO) - estado.distancia(IA)
    # Un poco de valor a guardar muros, para que no los gaste sin motivo.
    ventaja_muros = estado.muros_restantes[IA] - estado.muros_restantes[HUMANO]
    return 10 * ventaja_camino + ventaja_muros


def muros_candidatos(estado):
    """Muros que cortan algún paso del camino más corto del rival."""
    rival = 1 - estado.turno
    camino = estado.camino(rival)
    candidatos = set()

    # Recorremos el camino de dos en dos casillas: (desde, hasta).
    for (f1, c1), (f2, c2) in zip(camino, camino[1:]):
        if c1 == c2:
            # Paso vertical: lo cortan los muros horizontales justo debajo de la fila de arriba.
            f = min(f1, f2)
            candidatos.add(('h', f, c1))
            candidatos.add(('h', f, c1 - 1))
        else:
            # Paso horizontal: lo cortan los muros verticales justo a la derecha de la columna izquierda.
            c = min(c1, c2)
            candidatos.add(('v', f1, c))
            candidatos.add(('v', f1 - 1, c))

    return [muro for muro in sorted(candidatos) if estado.muro_valido(*muro)]


def movimientos_peon_utiles(estado):
    """Movimientos del peón que lo acercan a su meta (acortan su camino de A*).

    Sin este filtro la IA podía quedarse yendo y viniendo entre dos casillas:
    con poca profundidad siempre teme que el rival le ponga un muro si avanza,
    así que se aparta "por si acaso", y el turno siguiente vuelve a hacer lo mismo.
    Si ningún movimiento acerca (por ejemplo, el otro peón tapa el camino), se usan todos."""
    jugador = estado.turno
    distancia_ahora = estado.distancia(jugador)
    todos = [('mover', f, c) for f, c in estado.movimientos_peon(jugador)]
    utiles = [m for m in todos if estado.aplicar(m).distancia(jugador) < distancia_ahora]
    return utiles or todos


def generar_movimientos(estado):
    """Jugadas que el minimax va a probar: mover el peón hacia la meta + muros útiles."""
    jugadas = movimientos_peon_utiles(estado)
    if estado.muros_restantes[estado.turno] > 0:
        jugadas += muros_candidatos(estado)
    return jugadas


def minimax(estado, profundidad, alfa, beta):
    """Devuelve (puntuación, mejor jugada) para el jugador que tiene el turno."""
    if profundidad == 0 or estado.ganador() is not None:
        return evaluar(estado, profundidad), None

    jugadas = generar_movimientos(estado)
    mejor_jugada = None

    if estado.turno == IA:
        # Turno de MAX: buscamos la puntuación más alta.
        mejor = -math.inf
        for jugada in jugadas:
            puntuacion, _ = minimax(estado.aplicar(jugada), profundidad - 1, alfa, beta)
            if puntuacion > mejor:
                mejor, mejor_jugada = puntuacion, jugada
            alfa = max(alfa, mejor)
            if alfa >= beta:
                break  # poda: MIN nunca permitiría llegar aquí
    else:
        # Turno de MIN: buscamos la puntuación más baja.
        mejor = math.inf
        for jugada in jugadas:
            puntuacion, _ = minimax(estado.aplicar(jugada), profundidad - 1, alfa, beta)
            if puntuacion < mejor:
                mejor, mejor_jugada = puntuacion, jugada
            beta = min(beta, mejor)
            if alfa >= beta:
                break  # poda: MAX nunca permitiría llegar aquí

    return mejor, mejor_jugada


def mejor_movimiento(estado, profundidad=PROFUNDIDAD):
    """Punto de entrada para el juego: la jugada que elige la IA."""
    _, jugada = minimax(estado, profundidad, -math.inf, math.inf)
    return jugada
