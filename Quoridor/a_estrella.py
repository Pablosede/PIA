"""
a_estrella.py
-------------
El algoritmo A* (A estrella): busca el camino más corto de un peón hasta su fila meta.

Cómo funciona:
  1. Hay una lista de casillas "por visitar". Al principio solo está la del peón.
  2. Cada vez elegimos la casilla más prometedora: la de menor  f = g + h
       g = pasos que cuesta llegar a ella desde el inicio
       h = estimación de los pasos que faltan (las filas que quedan hasta la meta)
  3. Si esa casilla está en la fila meta, ya tenemos el camino.
  4. Si no, apuntamos sus vecinas (las que no tienen muro en medio) y repetimos.

Aquí también están las funciones que usan A*: camino(), distancia(), alguien_encerrado()
y muro_valido().
"""

from tablero import HUMANO, IA, FILA_META, vecinos, muro_cabe, aplicar


def a_estrella(muros, inicio, fila_meta):
    """Camino más corto (lista de casillas) desde 'inicio' hasta 'fila_meta', o None si no hay."""

    def h(casilla):
        # Filas que faltan hasta la meta. Nunca es más que los pasos de verdad,
        # y por eso A* encuentra siempre el camino más corto.
        return abs(casilla[0] - fila_meta)

    g = {inicio: 0}            # g de cada casilla: cuántos pasos cuesta llegar a ella
    f = {inicio: h(inicio)}    # f = g + h de cada casilla: cuanto más pequeño, más prometedora
    viene_de = {inicio: None}  # desde qué casilla llegamos a cada una
    por_visitar = [inicio]

    while por_visitar:
        # 1. Elegimos la casilla por visitar con menor f
        actual = por_visitar[0]
        for casilla in por_visitar:
            if f[casilla] < f[actual]:
                actual = casilla
        por_visitar.remove(actual)

        # 2. Si está en la fila meta, reconstruimos el camino yendo hacia atrás
        if actual[0] == fila_meta:
            camino = []
            while actual is not None:
                camino.insert(0, actual)
                actual = viene_de[actual]
            return camino

        # 3. Apuntamos sus vecinas (si es la primera vez que llegamos o llegamos con menos pasos)
        for vecina in vecinos(muros, actual):
            if vecina not in g or g[actual] + 1 < g[vecina]:
                g[vecina] = g[actual] + 1
                f[vecina] = g[vecina] + h(vecina)
                viene_de[vecina] = actual
                if vecina not in por_visitar:
                    por_visitar.append(vecina)

    return None  # nos quedamos sin casillas: no hay ningún camino


def camino(estado, jugador):
    """Camino más corto del jugador hasta su meta (None si no tiene ninguno).
    La primera vez se calcula con A* y se apunta en estado['caminos'];
    las siguientes veces se lee de ahí, sin volver a buscar."""
    if jugador not in estado['caminos']:
        estado['caminos'][jugador] = a_estrella(estado['muros'], estado['peones'][jugador], FILA_META[jugador])
    return estado['caminos'][jugador]


def distancia(estado, jugador):
    """Cuántos pasos le faltan al jugador para ganar."""
    return len(camino(estado, jugador)) - 1


def alguien_encerrado(estado):
    """¿Hay algún jugador sin ningún camino hasta su meta? (Las reglas no lo permiten.)"""
    return camino(estado, HUMANO) is None or camino(estado, IA) is None


def muro_valido(estado, muro):
    """Un muro se puede poner si cabe y si después los dos jugadores siguen teniendo camino."""
    return muro_cabe(estado, muro) and not alguien_encerrado(aplicar(estado, muro))
