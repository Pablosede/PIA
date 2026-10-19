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

import sys

import pygame

from tablero import Estado, TAMANO, HUMANO, IA, MUROS_INICIALES
from minimax import mejor_movimiento

# --- Medidas (en píxeles) ---
CELDA = 56                       # lado de una casilla
HUECO = 14                       # ancho del hueco entre casillas (donde van los muros)
PASO = CELDA + HUECO             # distancia entre el inicio de una casilla y la siguiente
MARGEN = 30                      # borde alrededor del tablero
LADO_TABLERO = TAMANO * CELDA + (TAMANO - 1) * HUECO
ALTO_PANEL = 90                  # zona de texto debajo del tablero
ANCHO = LADO_TABLERO + 2 * MARGEN
ALTO = LADO_TABLERO + 2 * MARGEN + ALTO_PANEL

# --- Colores (R, G, B) ---
FONDO = (60, 40, 30)
CASILLA = (205, 170, 125)
COLOR_JUGADOR = {HUMANO: (40, 110, 220), IA: (210, 50, 50)}
META = {HUMANO: (165, 175, 200), IA: (215, 150, 135)}  # filas meta teñidas con el color del jugador
COLOR_MURO = {HUMANO: (90, 160, 255), IA: (240, 90, 90)}  # cada jugador pinta sus muros de su color
PREVIA_OK = (120, 220, 120)
PREVIA_MAL = (120, 120, 120)  # gris, para no confundirlo con los muros rojos de la IA
POSIBLE = (90, 190, 90)
TEXTO = (240, 240, 240)


# ----------------------------------------------------------------------
# Conversión entre coordenadas del tablero y píxeles
# ----------------------------------------------------------------------

def rect_casilla(f, c):
    return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO, CELDA, CELDA)


def rect_muro(orientacion, f, c):
    if orientacion == 'h':  # debajo de las casillas (f, c) y (f, c+1)
        return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO + CELDA, 2 * CELDA + HUECO, HUECO)
    else:                   # a la derecha de las casillas (f, c) y (f+1, c)
        return pygame.Rect(MARGEN + c * PASO + CELDA, MARGEN + f * PASO, HUECO, 2 * CELDA + HUECO)


def raton_a_casilla(x, y):
    """Casilla (f, c) bajo el ratón, o None si está en un hueco o fuera."""
    c, resto_x = divmod(x - MARGEN, PASO)
    f, resto_y = divmod(y - MARGEN, PASO)
    if 0 <= f < TAMANO and 0 <= c < TAMANO and resto_x < CELDA and resto_y < CELDA:
        return f, c
    return None


def raton_a_muro(x, y):
    """Muro (orientación, f, c) que corresponde al hueco bajo el ratón, o None.
    En un hueco horizontal -> muro 'h'; en un hueco vertical -> muro 'v'.
    Como el muro mide 2 casillas, se coloca en las dos más cercanas al ratón.
    En el cruce de dos huecos no se elige ningún muro."""
    c, resto_x = divmod(x - MARGEN, PASO)
    f, resto_y = divmod(y - MARGEN, PASO)
    if not (0 <= f < TAMANO and 0 <= c < TAMANO):
        return None
    en_hueco_x = resto_x >= CELDA  # entre la columna c y la c+1
    en_hueco_y = resto_y >= CELDA  # entre la fila f y la f+1

    if en_hueco_y and not en_hueco_x and f < TAMANO - 1:
        if resto_x < CELDA // 2:  # ratón en la mitad izquierda: el muro empieza una columna antes
            c -= 1
        return ('h', f, max(0, min(c, TAMANO - 2)))

    if en_hueco_x and not en_hueco_y and c < TAMANO - 1:
        if resto_y < CELDA // 2:  # ratón en la mitad de arriba: el muro empieza una fila antes
            f -= 1
        return ('v', max(0, min(f, TAMANO - 2)), c)

    return None


def clic_a_movimiento(estado, pos):
    """Traduce un clic del humano a un movimiento legal, o None si no es válido."""
    casilla = raton_a_casilla(*pos)
    if casilla in estado.movimientos_peon(HUMANO):
        return ('mover', *casilla)
    muro = raton_a_muro(*pos)
    if muro and estado.muro_valido(*muro):
        return muro
    return None


# ----------------------------------------------------------------------
# Dibujo
# ----------------------------------------------------------------------

def dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos):
    pantalla.fill(FONDO)
    ganador = estado.ganador()
    turno_humano = estado.turno == HUMANO and ganador is None

    # Casillas (las filas meta se tiñen con el color de quien quiere llegar a ellas)
    for f in range(TAMANO):
        for c in range(TAMANO):
            color = META[HUMANO] if f == 0 else META[IA] if f == TAMANO - 1 else CASILLA
            pygame.draw.rect(pantalla, color, rect_casilla(f, c), border_radius=6)

    # Caminos más cortos calculados con A* (tecla C)
    if mostrar_caminos:
        for jugador in (HUMANO, IA):
            puntos = [rect_casilla(f, c).center for f, c in estado.camino(jugador)]
            if len(puntos) > 1:
                pygame.draw.lines(pantalla, COLOR_JUGADOR[jugador], False, puntos, 4)

    # Casillas a las que puede moverse el humano
    if turno_humano:
        for f, c in estado.movimientos_peon(HUMANO):
            pygame.draw.circle(pantalla, POSIBLE, rect_casilla(f, c).center, 10)

    # Muros colocados, cada uno del color del jugador que lo puso
    for (f, c), jugador in estado.muros_h.items():
        pygame.draw.rect(pantalla, COLOR_MURO[jugador], rect_muro('h', f, c), border_radius=4)
    for (f, c), jugador in estado.muros_v.items():
        pygame.draw.rect(pantalla, COLOR_MURO[jugador], rect_muro('v', f, c), border_radius=4)

    # Vista previa del muro bajo el ratón (verde si se puede poner, gris si no)
    if turno_humano:
        muro = raton_a_muro(*pygame.mouse.get_pos())
        if muro:
            color = PREVIA_OK if estado.muro_valido(*muro) else PREVIA_MAL
            pygame.draw.rect(pantalla, color, rect_muro(*muro), border_radius=4)

    # Peones
    for jugador in (HUMANO, IA):
        centro = rect_casilla(*estado.peones[jugador]).center
        pygame.draw.circle(pantalla, COLOR_JUGADOR[jugador], centro, CELDA // 2 - 8)
        pygame.draw.circle(pantalla, TEXTO, centro, CELDA // 2 - 8, 2)

    # Mensaje final: oscurecemos el tablero y anunciamos al ganador en grande
    if ganador is not None:
        velo = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
        velo.fill((0, 0, 0, 160))  # negro semitransparente (el 4º número es la transparencia)
        pantalla.blit(velo, (0, 0))
        centro_x, centro_y = ANCHO // 2, MARGEN + LADO_TABLERO // 2
        titulo = "¡HAS GANADO!" if ganador == HUMANO else "¡GANA LA IA!"
        texto = fuente_grande.render(titulo, True, COLOR_MURO[ganador])
        pantalla.blit(texto, texto.get_rect(center=(centro_x, centro_y - 20)))
        texto = fuente.render("Pulsa R para jugar otra vez", True, TEXTO)
        pantalla.blit(texto, texto.get_rect(center=(centro_x, centro_y + 35)))

    # Panel de información
    if ganador == HUMANO:
        mensaje = "¡Has ganado!  Pulsa R para jugar otra vez"
    elif ganador == IA:
        mensaje = "Gana la IA.  Pulsa R para jugar otra vez"
    elif estado.turno == HUMANO:
        mensaje = "Tu turno (azul): mueve o pon un muro en un hueco"
    else:
        mensaje = "La IA (rojo) está pensando..."

    lineas = [
        mensaje,
        f"Muros  -  Tú: {estado.muros_restantes[HUMANO]}/{MUROS_INICIALES}"
        f"     IA: {estado.muros_restantes[IA]}/{MUROS_INICIALES}",
        "C: caminos A*     R: reiniciar     ESC: salir",
    ]
    y = LADO_TABLERO + 2 * MARGEN - 10
    for linea in lineas:
        pantalla.blit(fuente.render(linea, True, TEXTO), (MARGEN, y))
        y += 28

    pygame.display.flip()


# ----------------------------------------------------------------------
# Bucle principal
# ----------------------------------------------------------------------

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Quoridor - Minimax con poda alfa-beta + A*")
    fuente = pygame.font.SysFont(None, 28)
    fuente_grande = pygame.font.SysFont(None, 80)  # para el mensaje final
    reloj = pygame.time.Clock()

    estado = Estado()
    mostrar_caminos = False

    while True:
        # 1. Leer teclado y ratón
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if evento.key == pygame.K_r:
                    estado = Estado()
                if evento.key == pygame.K_c:
                    mostrar_caminos = not mostrar_caminos
            if (evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1
                    and estado.turno == HUMANO and estado.ganador() is None):
                movimiento = clic_a_movimiento(estado, evento.pos)
                if movimiento:
                    estado = estado.aplicar(movimiento)

        # 2. Dibujar (antes de que piense la IA, para que se vea "pensando...")
        dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos)

        # 3. Turno de la IA
        if estado.turno == IA and estado.ganador() is None:
            estado = estado.aplicar(mejor_movimiento(estado))
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # ignora clics hechos mientras pensaba

        reloj.tick(30)  # máximo 30 fotogramas por segundo


if __name__ == "__main__":
    main()
