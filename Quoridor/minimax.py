"""
minimax.py
----------
La IA: Minimax con poda alfa-beta.

Minimax:
  - La IA prueba sus jugadas, después las respuestas del humano, después las suyas...
    hasta mirar PROFUNDIDAD turnos hacia delante.
  - Al final puntúa cómo ha quedado la partida con evaluar().
  - La IA (MAX) elige lo que da MÁS puntos y supone que el humano (MIN) elegirá lo que da MENOS.

Poda alfa-beta (para ir más rápido sin cambiar el resultado):
  - alfa = los puntos que la IA ya tiene asegurados con otra jugada.
  - beta = los puntos que el humano ya tiene asegurados con otra jugada.
  - Si alfa >= beta, a esta rama nunca se llegaría jugando bien, así que se deja de mirar.
"""

import math

from tablero import HUMANO, IA, aplicar, ganador, movimientos_peon, muros_que_bloquean, muro_cabe
from a_estrella import camino, distancia, alguien_encerrado

PROFUNDIDAD = 4  # turnos que mira hacia delante (con 2 es más fácil ganarle)
PESO_MUROS = 5   # lo que vale cada muro que le queda (un paso de ventaja vale 10)
VICTORIA = 1000  # puntos por ganar la partida


def evaluar(estado, profundidad):
    """Puntos de la partida para la IA: positivo = va ganando la IA, negativo = va ganando el humano."""
    if ganador(estado) == IA:
        return VICTORIA + profundidad  # + profundidad: cuanto antes gane, mejor
    if ganador(estado) == HUMANO:
        return -VICTORIA - profundidad

    pasos_humano = distancia(estado, HUMANO)
    pasos_ia = distancia(estado, IA)
    muros_humano = estado['muros_restantes'][HUMANO]
    muros_ia = estado['muros_restantes'][IA]
    return 10 * (pasos_humano - pasos_ia) + PESO_MUROS * (muros_ia - muros_humano)


def jugadas_a_probar(estado):
    """Las jugadas que se van a probar. No se prueban todas (hay unas 130), solo las útiles."""
    yo = estado['turno']
    rival = 1 - yo
    jugadas = []

    # 1) Mover el peón, pero solo a casillas que lo acercan a la meta.
    #    (Si no, la IA a veces se quedaba yendo y viniendo entre dos casillas.)
    pasos_ahora = distancia(estado, yo)
    for f, c in movimientos_peon(estado, yo):
        jugada = ('mover', f, c)
        if distancia(aplicar(estado, jugada), yo) < pasos_ahora:
            jugadas.append(jugada)
    if len(jugadas) == 0:
        # Ninguna acerca (por ejemplo, el rival tapa el paso): probamos todas.
        for f, c in movimientos_peon(estado, yo):
            jugadas.append(('mover', f, c))

    # 2) Poner un muro, pero solo los que cortan el camino más corto del rival
    #    (los demás no le retrasan). Van en el orden del camino, empezando por los que tiene
    #    más cerca: suelen ser los mejores, y probar primero lo mejor hace que la poda corte antes.
    #    Que no encierren a nadie lo comprueba minimax() al probarlos.
    if estado['muros_restantes'][yo] > 0:
        ruta = camino(estado, rival)
        muros = []
        for i in range(len(ruta) - 1):
            for muro in muros_que_bloquean(ruta[i], ruta[i + 1]): # muros que cortan ese paso
                if muro not in muros and muro_cabe(estado, muro): # sin repetir y que quepa
                    muros.append(muro)
        jugadas += muros  # se añaden después de los movimientos

    return jugadas


def minimax(estado, profundidad, alfa, beta):
    """Devuelve (puntos, mejor jugada) para el jugador al que le toca."""
    if profundidad == 0 or ganador(estado) is not None:
        return evaluar(estado, profundidad), None

    mejor_jugada = None

    if estado['turno'] == IA:
        # Turno de la IA (MAX): busca los MÁS puntos.
        mejor = -math.inf
        for jugada in jugadas_a_probar(estado):
            hijo = aplicar(estado, jugada)
            # Un muro que deja a alguien sin camino no vale. Se comprueba aquí, justo antes de
            # probarlo, para no perder tiempo con las jugadas que la poda no llega a mirar.
            if alguien_encerrado(hijo):
                continue
            puntos, _ = minimax(hijo, profundidad - 1, alfa, beta)  # _ = su mejor jugada, aquí no hace falta
            if puntos > mejor:
                mejor = puntos
                mejor_jugada = jugada
            alfa = max(alfa, mejor)
            if alfa >= beta:
                break  # poda: el humano nunca dejaría llegar aquí
    else:
        # Turno del humano (MIN): busca los MENOS puntos.
        mejor = math.inf
        for jugada in jugadas_a_probar(estado):
            hijo = aplicar(estado, jugada)
            if alguien_encerrado(hijo):
                continue
            puntos, _ = minimax(hijo, profundidad - 1, alfa, beta)
            if puntos < mejor:
                mejor = puntos
                mejor_jugada = jugada
            beta = min(beta, mejor)
            if alfa >= beta:
                break  # poda: la IA nunca dejaría llegar aquí

    return mejor, mejor_jugada


def mejor_movimiento(estado, profundidad=PROFUNDIDAD):
    """La jugada que elige la IA."""
    puntos, jugada = minimax(estado, profundidad, -math.inf, math.inf)
    return jugada
