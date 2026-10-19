"""
tablero.py
----------
Las reglas del Quoridor: el estado de la partida, cómo se mueven los
peones y cómo se colocan los muros.

Coordenadas:
  - El tablero tiene 9x9 casillas. Una casilla es (fila, columna) y la
    (0, 0) es la de arriba a la izquierda.
  - Los muros miden 2 casillas y se colocan en los huecos entre ellas.
    Un muro se identifica por su orientación y por la casilla (f, c)
    donde empieza (arriba a la izquierda del muro):
      * 'h' (horizontal): queda debajo de (f, c) y (f, c+1).
                          Bloquea el paso entre la fila f y la f+1.
      * 'v' (vertical):   queda a la derecha de (f, c) y (f+1, c).
                          Bloquea el paso entre la columna c y la c+1.
    Por eso f y c de un muro van de 0 a 7.

Movimientos (tuplas de 3 elementos):
  - ('mover', f, c) -> mover el peón a la casilla (f, c)
  - ('h', f, c)     -> poner un muro horizontal en (f, c)
  - ('v', f, c)     -> poner un muro vertical en (f, c)
"""

from a_estrella import a_estrella

TAMANO = 9            # casillas por lado
MUROS_INICIALES = 10  # muros que tiene cada jugador al empezar

HUMANO = 0  # empieza abajo y tiene que llegar a la fila de arriba
IA = 1      # empieza arriba y tiene que llegar a la fila de abajo
FILA_META = {HUMANO: 0, IA: TAMANO - 1}

DIRECCIONES = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izquierda, derecha


class Estado:
    """Todo lo que hace falta saber de una partida en un momento dado."""

    def __init__(self):
        self.peones = [(TAMANO - 1, TAMANO // 2), (0, TAMANO // 2)]  # [humano, IA]
        self.muros_restantes = [MUROS_INICIALES, MUROS_INICIALES]
        # Muros colocados: diccionarios {(f, c): jugador que lo puso}.
        # Guardamos el jugador para poder pintar cada muro de su color.
        self.muros_h = {}  # horizontales
        self.muros_v = {}  # verticales
        self.turno = HUMANO

    def copiar(self):
        """Copia independiente del estado (el minimax prueba jugadas sobre copias)."""
        nuevo = Estado()
        nuevo.peones = list(self.peones)
        nuevo.muros_restantes = list(self.muros_restantes)
        nuevo.muros_h = dict(self.muros_h)
        nuevo.muros_v = dict(self.muros_v)
        nuevo.turno = self.turno
        return nuevo

    # ------------------------------------------------------------------
    # Muros y paso entre casillas
    # ------------------------------------------------------------------

    def hay_muro_entre(self, a, b):
        """¿Hay un muro entre dos casillas vecinas a y b?"""
        (f1, c1), (f2, c2) = a, b
        if c1 == c2:
            # Paso vertical: lo cortaría un muro horizontal bajo la fila de arriba.
            # Ese muro puede empezar en la columna c o en la c-1 (mide 2 casillas).
            f = min(f1, f2)
            return (f, c1) in self.muros_h or (f, c1 - 1) in self.muros_h
        else:
            # Paso horizontal: lo cortaría un muro vertical a la derecha de la columna izquierda.
            # Ese muro puede empezar en la fila f o en la f-1.
            c = min(c1, c2)
            return (f1, c) in self.muros_v or (f1 - 1, c) in self.muros_v

    def puede_pasar(self, a, b):
        """¿Se puede ir de la casilla a a su vecina b? (b dentro del tablero y sin muro)."""
        f, c = b
        return 0 <= f < TAMANO and 0 <= c < TAMANO and not self.hay_muro_entre(a, b)

    def vecinos(self, casilla):
        """Casillas a las que se llega en un paso, ignorando los peones. Lo usa A*."""
        f, c = casilla
        return [(f + df, c + dc) for df, dc in DIRECCIONES
                if self.puede_pasar(casilla, (f + df, c + dc))]

    def camino(self, jugador):
        """Camino más corto (A*) del jugador hasta su meta, o None si no existe."""
        return a_estrella(self, self.peones[jugador], FILA_META[jugador])

    def distancia(self, jugador):
        """Número de pasos que le faltan al jugador para ganar."""
        return len(self.camino(jugador)) - 1

    def muro_valido(self, orientacion, f, c):
        """¿Puede el jugador que tiene el turno poner este muro?"""
        if self.muros_restantes[self.turno] == 0:
            return False
        if not (0 <= f < TAMANO - 1 and 0 <= c < TAMANO - 1):
            return False

        # No puede solaparse con otro muro igual ni cruzarse con uno perpendicular
        # (un muro 'h' y uno 'v' en la misma (f, c) forman una cruz).
        if orientacion == 'h':
            if any(m in self.muros_h for m in [(f, c - 1), (f, c), (f, c + 1)]) or (f, c) in self.muros_v:
                return False
        else:
            if any(m in self.muros_v for m in [(f - 1, c), (f, c), (f + 1, c)]) or (f, c) in self.muros_h:
                return False

        # No puede dejar a ningún jugador sin camino hasta su meta.
        # Lo ponemos de prueba, comprobamos con A* y lo quitamos.
        muros = self.muros_h if orientacion == 'h' else self.muros_v
        muros[(f, c)] = self.turno
        ambos_tienen_camino = self.camino(HUMANO) is not None and self.camino(IA) is not None
        del muros[(f, c)]
        return ambos_tienen_camino

    # ------------------------------------------------------------------
    # Movimiento de los peones
    # ------------------------------------------------------------------

    def movimientos_peon(self, jugador):
        """Casillas a las que puede ir el peón del jugador, incluyendo saltos."""
        yo = self.peones[jugador]
        rival = self.peones[1 - jugador]
        destinos = []

        for df, dc in DIRECCIONES:
            vecina = (yo[0] + df, yo[1] + dc)
            if not self.puede_pasar(yo, vecina):
                continue
            if vecina != rival:
                destinos.append(vecina)  # paso normal
                continue

            # El rival está justo al lado: intentamos saltar por encima en línea recta.
            detras = (vecina[0] + df, vecina[1] + dc)
            if self.puede_pasar(vecina, detras):
                destinos.append(detras)
            else:
                # Detrás hay muro o borde: se puede saltar en diagonal (a los lados del rival).
                for lado in [(dc, df), (-dc, -df)]:  # las dos direcciones perpendiculares
                    diagonal = (vecina[0] + lado[0], vecina[1] + lado[1])
                    if self.puede_pasar(vecina, diagonal):
                        destinos.append(diagonal)

        return destinos

    # ------------------------------------------------------------------
    # Jugadas y final de partida
    # ------------------------------------------------------------------

    def aplicar(self, movimiento):
        """Devuelve un estado NUEVO con el movimiento hecho y el turno pasado al rival."""
        tipo, f, c = movimiento
        nuevo = self.copiar()
        if tipo == 'mover':
            nuevo.peones[self.turno] = (f, c)
        else:
            muros = nuevo.muros_h if tipo == 'h' else nuevo.muros_v
            muros[(f, c)] = self.turno  # recordamos quién lo ha puesto
            nuevo.muros_restantes[self.turno] -= 1
        nuevo.turno = 1 - self.turno
        return nuevo

    def ganador(self):
        """HUMANO o IA si alguno ha llegado a su meta; None si la partida sigue."""
        for jugador in (HUMANO, IA):
            if self.peones[jugador][0] == FILA_META[jugador]:
                return jugador
        return None
