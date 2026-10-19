"""
tablero.py
----------
Las reglas del Quoridor y el algoritmo A*.

La partida se guarda en un diccionario (el "estado"):
    estado = {
        'peones': [(8, 4), (0, 4)],     # casilla (fila, columna) de cada jugador: [humano, IA]
        'muros': {('h', 3, 4): 0, ...},  # muros puestos -> jugador que lo puso
        'muros_restantes': [10, 10],
        'turno': 0,                      # a quién le toca: HUMANO (0) o IA (1)
    }
Un estado nunca se modifica: cada jugada crea uno nuevo con aplicar().

Casillas: (fila, columna) de 0 a 8. La (0, 0) es la de arriba a la izquierda.

Muros: miden 2 casillas y van en los huecos. Un muro es (orientación, f, c),
donde (f, c) es la casilla de arriba a la izquierda del muro (f y c de 0 a 7):
    ('h', f, c) horizontal: debajo de (f, c) y (f, c+1)
    ('v', f, c) vertical:   a la derecha de (f, c) y (f+1, c)

Jugadas: ('mover', f, c) para mover el peón, o un muro ('h', f, c) / ('v', f, c).
"""

import heapq
from functools import lru_cache

TAMANO = 9
MUROS_INICIALES = 10
HUMANO = 0  # empieza abajo y tiene que llegar a la fila 0
IA = 1      # empieza arriba y tiene que llegar a la fila 8
FILA_META = [0, TAMANO - 1]  # fila meta de cada jugador
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha


def nueva_partida():
    return {
        'peones': [(TAMANO - 1, TAMANO // 2), (0, TAMANO // 2)],
        'muros': {},
        'muros_restantes': [MUROS_INICIALES, MUROS_INICIALES],
        'turno': HUMANO,
    }


def aplicar(estado, jugada):
    """Devuelve un estado NUEVO con la jugada hecha y el turno pasado al rival."""
    yo = estado['turno']
    nuevo = {
        'peones': list(estado['peones']),
        'muros': dict(estado['muros']),
        'muros_restantes': list(estado['muros_restantes']),
        'turno': 1 - yo,
    }
    if jugada[0] == 'mover':
        nuevo['peones'][yo] = jugada[1:]  # (f, c)
    else:
        nuevo['muros'][jugada] = yo  # guardamos quién lo puso, para pintarlo de su color
        nuevo['muros_restantes'][yo] -= 1
    return nuevo


def ganador(estado):
    """HUMANO o IA si alguno ha llegado a su meta; None si la partida sigue."""
    for jugador in (HUMANO, IA):
        if estado['peones'][jugador][0] == FILA_META[jugador]:
            return jugador
    return None


# ----------------------------------------------------------------------
# Muros y paso entre casillas
# ----------------------------------------------------------------------

def muros_que_bloquean(a, b):
    """Los dos muros que cortarían el paso entre las casillas vecinas a y b.
    Son dos porque un muro mide 2 casillas: puede empezar a la altura de a o una antes."""
    (f1, c1), (f2, c2) = a, b
    if c1 == c2:  # paso arriba/abajo: muro horizontal debajo de la fila de arriba
        f = min(f1, f2)
        return [('h', f, c1), ('h', f, c1 - 1)]
    else:         # paso izquierda/derecha: muro vertical a la derecha de la columna izquierda
        c = min(c1, c2)
        return [('v', f1, c), ('v', f1 - 1, c)]


def puede_pasar(muros, a, b):
    """¿Se puede ir de la casilla a a su vecina b? (b dentro del tablero y sin muro en medio)."""
    f, c = b
    dentro = 0 <= f < TAMANO and 0 <= c < TAMANO
    return dentro and not any(m in muros for m in muros_que_bloquean(a, b))


def vecinos(muros, casilla):
    """Casillas a las que se llega en un paso, sin tener en cuenta los peones."""
    f, c = casilla
    return [(f + df, c + dc) for df, dc in DIRECCIONES if puede_pasar(muros, casilla, (f + df, c + dc))]


def muro_valido(estado, muro):
    """¿Puede el jugador con turno poner este muro?"""
    orientacion, f, c = muro
    if estado['muros_restantes'][estado['turno']] == 0:
        return False
    if not (0 <= f < TAMANO - 1 and 0 <= c < TAMANO - 1):
        return False

    # No puede pisar otro muro igual ni cruzarse en "+" con uno perpendicular.
    if orientacion == 'h':
        choques = [('h', f, c - 1), ('h', f, c), ('h', f, c + 1), ('v', f, c)]
    else:
        choques = [('v', f - 1, c), ('v', f, c), ('v', f + 1, c), ('h', f, c)]
    if any(m in estado['muros'] for m in choques):
        return False

    # No puede dejar a ningún jugador sin camino hasta su meta (lo comprobamos con A*).
    prueba = aplicar(estado, muro)
    return camino(prueba, HUMANO) is not None and camino(prueba, IA) is not None


# ----------------------------------------------------------------------
# Movimiento de los peones
# ----------------------------------------------------------------------

def movimientos_peon(estado, jugador):
    """Casillas a las que puede ir el peón del jugador, incluyendo saltos."""
    muros = estado['muros']
    yo = estado['peones'][jugador]
    rival = estado['peones'][1 - jugador]
    destinos = []

    for df, dc in DIRECCIONES:
        vecina = (yo[0] + df, yo[1] + dc)
        if not puede_pasar(muros, yo, vecina):
            continue
        if vecina != rival:
            destinos.append(vecina)  # paso normal
            continue

        # El rival está justo al lado: intentamos saltar por encima en línea recta.
        detras = (vecina[0] + df, vecina[1] + dc)
        if puede_pasar(muros, vecina, detras):
            destinos.append(detras)
        else:
            # Detrás hay muro o borde: se puede saltar en diagonal (a los lados del rival).
            for lado in [(dc, df), (-dc, -df)]:  # las dos direcciones perpendiculares
                diagonal = (vecina[0] + lado[0], vecina[1] + lado[1])
                if puede_pasar(muros, vecina, diagonal):
                    destinos.append(diagonal)

    return destinos


# ----------------------------------------------------------------------
# A* (A estrella): camino más corto de un peón hasta su fila meta
# ----------------------------------------------------------------------

def camino(estado, jugador):
    """Camino más corto del jugador hasta su meta (lista de casillas), o None si no hay."""
    # frozenset: un conjunto que no se puede modificar, para que @lru_cache pueda guardarlo.
    return a_estrella(frozenset(estado['muros']), estado['peones'][jugador], FILA_META[jugador])


def distancia(estado, jugador):
    """Número de pasos que le faltan al jugador para ganar."""
    return len(camino(estado, jugador)) - 1


@lru_cache(maxsize=50_000)  # recuerda los últimos resultados para no repetir la misma búsqueda
def a_estrella(muros, inicio, fila_meta):
    """A*: siempre expande primero la casilla con menor f = g + h, donde
      g = pasos dados desde el inicio
      h = filas que faltan hasta la meta (heurística: nunca sobreestima,
          porque cada paso avanza como mucho una fila; así el camino es el más corto)."""
    abiertos = [(abs(inicio[0] - fila_meta), 0, inicio)]  # cola de prioridad con (f, g, casilla)
    pasos = {inicio: 0}     # g: menor número de pasos conocido hasta cada casilla
    padre = {inicio: None}  # de dónde venimos, para reconstruir el camino al final

    while abiertos:
        _, g, actual = heapq.heappop(abiertos)

        if actual[0] == fila_meta:  # ¡meta! reconstruimos el camino hacia atrás
            ruta = []
            while actual is not None:
                ruta.append(actual)
                actual = padre[actual]
            return ruta[::-1]

        if g > pasos[actual]:
            continue  # ya habíamos llegado aquí por un camino más corto

        for vecino in vecinos(muros, actual):
            if vecino not in pasos or g + 1 < pasos[vecino]:
                pasos[vecino] = g + 1
                padre[vecino] = actual
                h = abs(vecino[0] - fila_meta)
                heapq.heappush(abiertos, (g + 1 + h, g + 1, vecino))

    return None  # no hay ningún camino
