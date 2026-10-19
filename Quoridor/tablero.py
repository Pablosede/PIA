"""
tablero.py
----------
Las reglas del juego.

La partida se guarda en un diccionario que llamamos "estado":
    estado['peones']           -> dónde está cada peón: [peón del humano, peón de la IA]
    estado['muros']            -> los muros puestos y quién puso cada uno
    estado['muros_restantes']  -> cuántos muros le quedan a cada uno
    estado['turno']            -> a quién le toca: HUMANO (0) o IA (1)
    estado['caminos']          -> caminos más cortos ya calculados con A* (los apunta a_estrella.camino)

Casillas: (fila, columna), de 0 a 8. La (0, 0) es la de arriba a la izquierda.

Muros: miden 2 casillas y se escriben (tipo, fila, columna):
    ('h', f, c) -> muro horizontal debajo de las casillas (f, c) y (f, c+1)
    ('v', f, c) -> muro vertical a la derecha de las casillas (f, c) y (f+1, c)

Jugadas:
    ('mover', f, c)            -> mover el peón a la casilla (f, c)
    ('h', f, c) o ('v', f, c)  -> poner ese muro
"""

TAMANO = 9            # el tablero es de 9x9 casillas
MUROS_INICIALES = 10  # muros que tiene cada jugador al empezar
HUMANO = 0
IA = 1
FILA_META = [0, 8]    # el humano tiene que llegar a la fila 0 y la IA a la fila 8
DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha


def nueva_partida():
    """El estado al empezar: cada peón en el centro de su lado y sin muros."""
    return {
        'peones': [(8, 4), (0, 4)],
        'muros': {},
        'muros_restantes': [MUROS_INICIALES, MUROS_INICIALES],
        'turno': HUMANO,
        'caminos': {},
    }


def aplicar(estado, jugada):
    """Hace una jugada y devuelve el estado nuevo.
    El estado antiguo no se toca: así el minimax puede probar jugadas sin estropear la partida."""
    yo = estado['turno']
    rival = 1 - yo
    nuevo = {
        'peones': list(estado['peones']),  # list() y dict() hacen copias
        'muros': dict(estado['muros']),
        'muros_restantes': list(estado['muros_restantes']),
        'turno': rival,  # ahora le toca al otro
        'caminos': {},   # en el estado nuevo hay que volver a calcular los caminos
    }
    tipo, f, c = jugada
    if tipo == 'mover':
        nuevo['peones'][yo] = (f, c)
        # Mover un peón no cambia el camino del rival (A* no tiene en cuenta los peones): lo copiamos.
        if rival in estado['caminos']:
            nuevo['caminos'][rival] = estado['caminos'][rival]
    else:
        nuevo['muros'][jugada] = yo  # apuntamos quién lo puso (para pintarlo de su color)
        nuevo['muros_restantes'][yo] -= 1
    return nuevo


def ganador(estado):
    """Devuelve HUMANO o IA si alguno ha llegado a su meta, o None si la partida sigue."""
    if estado['peones'][HUMANO][0] == FILA_META[HUMANO]:
        return HUMANO
    if estado['peones'][IA][0] == FILA_META[IA]:
        return IA
    return None


def muros_que_bloquean(a, b):
    """Los dos muros que cortarían el paso entre dos casillas vecinas a y b.
    Son dos porque un muro mide 2 casillas: puede empezar aquí o una casilla antes."""
    fa, ca = a
    fb, cb = b
    if ca == cb:
        # Paso de arriba a abajo: lo corta un muro horizontal debajo de la fila de arriba.
        f = min(fa, fb)
        return [('h', f, ca), ('h', f, ca - 1)]
    else:
        # Paso de izquierda a derecha: lo corta un muro vertical a la derecha de la columna izquierda.
        c = min(ca, cb)
        return [('v', fa, c), ('v', fa - 1, c)]


def puede_pasar(muros, a, b):
    """¿Se puede ir de la casilla a a su vecina b? (b tiene que estar dentro y sin muro en medio)."""
    fb, cb = b
    if fb < 0 or fb >= TAMANO or cb < 0 or cb >= TAMANO:
        return False  # fuera del tablero
    for muro in muros_que_bloquean(a, b):
        if muro in muros:
            return False  # hay un muro en medio
    return True


def vecinos(muros, casilla):
    """Casillas a las que se llega en un paso desde 'casilla' (sin contar los peones)."""
    f, c = casilla
    resultado = []
    for df, dc in DIRECCIONES:
        vecina = (f + df, c + dc)
        if puede_pasar(muros, casilla, vecina):
            resultado.append(vecina)
    return resultado


def muro_cabe(estado, muro):
    """¿Hay sitio para este muro? (le quedan muros, está dentro y no choca con otro).
    Ojo: falta comprobar que no encierra a nadie; eso lo hace muro_valido() en a_estrella.py."""
    tipo, f, c = muro
    if estado['muros_restantes'][estado['turno']] == 0:
        return False
    if f < 0 or f > TAMANO - 2 or c < 0 or c > TAMANO - 2:
        return False

    # Muros con los que chocaría: los del mismo tipo que se montan encima y el que lo cruza en "+".
    if tipo == 'h':
        choques = [('h', f, c - 1), ('h', f, c), ('h', f, c + 1), ('v', f, c)]
    else:
        choques = [('v', f - 1, c), ('v', f, c), ('v', f + 1, c), ('h', f, c)]
    for otro in choques:
        if otro in estado['muros']:
            return False
    return True


def movimientos_peon(estado, jugador):
    """Casillas a las que puede moverse el peón del jugador (incluye los saltos)."""
    muros = estado['muros']
    yo = estado['peones'][jugador]
    rival = estado['peones'][1 - jugador]
    destinos = []

    for df, dc in DIRECCIONES:
        vecina = (yo[0] + df, yo[1] + dc)
        if not puede_pasar(muros, yo, vecina):
            continue  # muro o borde

        if vecina != rival:
            destinos.append(vecina)  # casilla libre: paso normal
            continue

        # El rival está en esa casilla: saltamos por encima de él.
        detras = (vecina[0] + df, vecina[1] + dc)
        if puede_pasar(muros, vecina, detras):
            destinos.append(detras)  # salto recto
        else:
            # Detrás del rival hay muro o borde: se salta en diagonal, a un lado del rival.
            if df == 0:
                lados = [(-1, 0), (1, 0)]  # íbamos en horizontal: los lados son arriba y abajo
            else:
                lados = [(0, -1), (0, 1)]  # íbamos en vertical: los lados son izquierda y derecha
            for lf, lc in lados:
                diagonal = (vecina[0] + lf, vecina[1] + lc)
                if puede_pasar(muros, vecina, diagonal):
                    destinos.append(diagonal)

    return destinos
