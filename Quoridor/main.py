"""
main.py
-------
Interfaz gráfica con pygame. Ejecuta este archivo para jugar:

    python main.py

Controles:
  - Clic en una casilla marcada        -> mover tu peón
  - Clic en un hueco entre casillas    -> poner un muro (se ve una vista previa)
  - C                                  -> mostrar/ocultar los caminos de A*
  - R                                  -> reiniciar la partida
  - ESC                                -> salir
"""

import pygame

from tablero import (TAMANO, HUMANO, IA, MUROS_INICIALES, nueva_partida, aplicar,
                     ganador, camino, movimientos_peon, muro_valido)
from minimax import mejor_movimiento

# --- Medidas (en píxeles) ---
CELDA = 56                       # lado de una casilla
HUECO = 14                       # ancho del hueco entre casillas (donde van los muros)
PASO = CELDA + HUECO             # distancia entre el inicio de una casilla y la siguiente
MARGEN = 30                      # borde alrededor del tablero
LADO_TABLERO = TAMANO * CELDA + (TAMANO - 1) * HUECO
ANCHO = LADO_TABLERO + 2 * MARGEN
ALTO = ANCHO + 90                # + panel de texto debajo del tablero

# --- Colores (R, G, B) ---
FONDO = (60, 40, 30)
CASILLA = (205, 170, 125)
COLOR_PEON = {HUMANO: (40, 110, 220), IA: (210, 50, 50)}
COLOR_MURO = {HUMANO: (90, 160, 255), IA: (240, 90, 90)}   # cada uno pinta sus muros de su color
COLOR_META = {HUMANO: (165, 175, 200), IA: (215, 150, 135)}  # fila a la que tiene que llegar cada uno
PREVIA_OK = (120, 220, 120)
PREVIA_MAL = (120, 120, 120)  # gris, para no confundirlo con los muros rojos de la IA
POSIBLE = (90, 190, 90)
TEXTO = (240, 240, 240)


# ----------------------------------------------------------------------
# Píxeles <-> tablero
# ----------------------------------------------------------------------

def rect_casilla(f, c):
    return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO, CELDA, CELDA)


def rect_muro(orientacion, f, c):
    if orientacion == 'h':  # debajo de las casillas (f, c) y (f, c+1)
        return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO + CELDA, 2 * CELDA + HUECO, HUECO)
    else:                   # a la derecha de las casillas (f, c) y (f+1, c)
        return pygame.Rect(MARGEN + c * PASO + CELDA, MARGEN + f * PASO, HUECO, 2 * CELDA + HUECO)


def raton_a_jugada(x, y):
    """Jugada que corresponde a la posición del ratón, o None:
      - sobre una casilla           -> ('mover', f, c)
      - sobre un hueco horizontal   -> muro 'h' (en las dos casillas más cercanas al ratón)
      - sobre un hueco vertical     -> muro 'v'
      - en el cruce de dos huecos o fuera del tablero -> None"""
    c, resto_x = divmod(x - MARGEN, PASO)
    f, resto_y = divmod(y - MARGEN, PASO)
    if not (0 <= f < TAMANO and 0 <= c < TAMANO):
        return None
    en_hueco_x = resto_x >= CELDA  # entre la columna c y la c+1
    en_hueco_y = resto_y >= CELDA  # entre la fila f y la f+1

    if not en_hueco_x and not en_hueco_y:
        return ('mover', f, c)
    if en_hueco_y and not en_hueco_x and f < TAMANO - 1:
        if resto_x < CELDA // 2:  # ratón en la mitad izquierda: el muro empieza una columna antes
            c -= 1
        return ('h', f, max(0, min(c, TAMANO - 2)))
    if en_hueco_x and not en_hueco_y and c < TAMANO - 1:
        if resto_y < CELDA // 2:  # ratón en la mitad de arriba: el muro empieza una fila antes
            f -= 1
        return ('v', max(0, min(f, TAMANO - 2)), c)
    return None


def es_legal(estado, jugada):
    """¿Puede el humano hacer esta jugada ahora?"""
    if jugada is None:
        return False
    if jugada[0] == 'mover':
        return jugada[1:] in movimientos_peon(estado, HUMANO)
    return muro_valido(estado, jugada)


# ----------------------------------------------------------------------
# Dibujo
# ----------------------------------------------------------------------

def dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos):
    pantalla.fill(FONDO)
    quien_gana = ganador(estado)
    turno_humano = estado['turno'] == HUMANO and quien_gana is None

    # Casillas (las filas meta se tiñen con el color de quien tiene que llegar a ellas)
    for f in range(TAMANO):
        for c in range(TAMANO):
            color = COLOR_META[HUMANO] if f == 0 else COLOR_META[IA] if f == TAMANO - 1 else CASILLA
            pygame.draw.rect(pantalla, color, rect_casilla(f, c), border_radius=6)

    # Caminos más cortos calculados con A* (tecla C)
    if mostrar_caminos:
        for jugador in (HUMANO, IA):
            puntos = [rect_casilla(f, c).center for f, c in camino(estado, jugador)]
            if len(puntos) > 1:
                pygame.draw.lines(pantalla, COLOR_PEON[jugador], False, puntos, 4)

    # Casillas a las que puede moverse el humano
    if turno_humano:
        for f, c in movimientos_peon(estado, HUMANO):
            pygame.draw.circle(pantalla, POSIBLE, rect_casilla(f, c).center, 10)

    # Muros puestos, cada uno del color del jugador que lo puso
    for muro, jugador in estado['muros'].items():
        pygame.draw.rect(pantalla, COLOR_MURO[jugador], rect_muro(*muro), border_radius=4)

    # Vista previa del muro bajo el ratón (verde si se puede poner, gris si no)
    jugada = raton_a_jugada(*pygame.mouse.get_pos())
    if turno_humano and jugada and jugada[0] != 'mover':
        color = PREVIA_OK if muro_valido(estado, jugada) else PREVIA_MAL
        pygame.draw.rect(pantalla, color, rect_muro(*jugada), border_radius=4)

    # Peones
    for jugador in (HUMANO, IA):
        centro = rect_casilla(*estado['peones'][jugador]).center
        pygame.draw.circle(pantalla, COLOR_PEON[jugador], centro, CELDA // 2 - 8)
        pygame.draw.circle(pantalla, TEXTO, centro, CELDA // 2 - 8, 2)

    # Mensaje final: oscurecemos todo y anunciamos al ganador en grande
    if quien_gana is not None:
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 160))  # negro semitransparente (el 4º número es la transparencia)
        pantalla.blit(velo, (0, 0))
        centro = (ANCHO // 2, MARGEN + LADO_TABLERO // 2)
        titulo = "¡HAS GANADO!" if quien_gana == HUMANO else "¡GANA LA IA!"
        texto = fuente_grande.render(titulo, True, COLOR_MURO[quien_gana])
        pantalla.blit(texto, texto.get_rect(center=(centro[0], centro[1] - 20)))
        texto = fuente.render("Pulsa R para jugar otra vez", True, TEXTO)
        pantalla.blit(texto, texto.get_rect(center=(centro[0], centro[1] + 35)))

    # Panel de información
    if quien_gana is not None:
        mensaje = "Fin de la partida"
    elif turno_humano:
        mensaje = "Tu turno (azul): mueve o pon un muro en un hueco"
    else:
        mensaje = "La IA (rojo) está pensando..."
    lineas = [
        mensaje,
        f"Muros  -  Tú: {estado['muros_restantes'][HUMANO]}/{MUROS_INICIALES}"
        f"     IA: {estado['muros_restantes'][IA]}/{MUROS_INICIALES}",
        "C: caminos A*     R: reiniciar     ESC: salir",
    ]
    for i, linea in enumerate(lineas):
        pantalla.blit(fuente.render(linea, True, TEXTO), (MARGEN, ANCHO - 10 + 28 * i))

    pygame.display.flip()


# ----------------------------------------------------------------------
# Bucle principal
# ----------------------------------------------------------------------

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Quoridor - Minimax con poda alfa-beta + A*")
    fuente = pygame.font.SysFont(None, 28)
    fuente_grande = pygame.font.SysFont(None, 80)
    reloj = pygame.time.Clock()

    estado = nueva_partida()
    mostrar_caminos = False

    while True:
        # 1. Leer teclado y ratón
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE):
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_r:
                estado = nueva_partida()
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_c:
                mostrar_caminos = not mostrar_caminos
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                jugada = raton_a_jugada(*evento.pos)
                if estado['turno'] == HUMANO and ganador(estado) is None and es_legal(estado, jugada):
                    estado = aplicar(estado, jugada)

        # 2. Dibujar (antes de que piense la IA, para que se vea "pensando...")
        dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos)

        # 3. Turno de la IA
        if estado['turno'] == IA and ganador(estado) is None:
            estado = aplicar(estado, mejor_movimiento(estado))
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # ignora clics hechos mientras pensaba

        reloj.tick(30)  # como mucho 30 fotogramas por segundo


if __name__ == "__main__":
    main()
