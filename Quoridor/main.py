"""
main.py
-------
La ventana del juego, hecha con pygame. Para jugar:

    python main.py

Controles:
  - Clic en una casilla con punto verde  -> mover tu peón
  - Clic en un hueco entre casillas      -> poner un muro (antes se ve en verde si se puede)
  - C                                    -> ver/ocultar los caminos que calcula A*
  - R                                    -> empezar otra partida
  - ESC                                  -> salir
"""

import pygame

from tablero import TAMANO, HUMANO, IA, MUROS_INICIALES, nueva_partida, aplicar, ganador, movimientos_peon
from a_estrella import camino, muro_valido
from minimax import mejor_movimiento

# --- Tamaños en píxeles ---
CELDA = 56                 # lado de una casilla
HUECO = 14                 # hueco entre casillas (donde van los muros)
PASO = CELDA + HUECO       # de una casilla a la siguiente
MARGEN = 30                # borde alrededor del tablero
LADO_TABLERO = TAMANO * CELDA + (TAMANO - 1) * HUECO
ANCHO = LADO_TABLERO + 2 * MARGEN
ALTO = ANCHO + 90          # 90 píxeles más para el texto de abajo

# --- Colores (rojo, verde, azul) ---
FONDO = (60, 40, 30)
CASILLA = (205, 170, 125)
COLOR_PEON = [(40, 110, 220), (210, 50, 50)]     # [humano azul, IA roja]
COLOR_MURO = [(90, 160, 255), (240, 90, 90)]     # los muros, del color de quien los puso
COLOR_META = [(165, 175, 200), (215, 150, 135)]  # la fila a la que tiene que llegar cada uno
VERDE = (100, 200, 100)
GRIS = (120, 120, 120)
BLANCO = (240, 240, 240)
NEGRO = (0, 0, 0)


def rect_casilla(f, c):
    """El rectángulo (en píxeles) de la casilla (f, c)."""
    return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO, CELDA, CELDA)


def rect_muro(tipo, f, c):
    """El rectángulo (en píxeles) de un muro."""
    if tipo == 'h':  # debajo de las casillas (f, c) y (f, c+1)
        return pygame.Rect(MARGEN + c * PASO, MARGEN + f * PASO + CELDA, 2 * CELDA + HUECO, HUECO)
    else:            # a la derecha de las casillas (f, c) y (f+1, c)
        return pygame.Rect(MARGEN + c * PASO + CELDA, MARGEN + f * PASO, HUECO, 2 * CELDA + HUECO)


def raton_a_jugada(x, y):
    """Qué jugada hay debajo del ratón:
      - encima de una casilla         -> mover a esa casilla
      - en el hueco de debajo         -> muro horizontal que empieza en esa casilla
      - en el hueco de la derecha     -> muro vertical que empieza en esa casilla
      - en un cruce de huecos o fuera -> None (nada)"""
    columna = (x - MARGEN) // PASO
    fila = (y - MARGEN) // PASO
    if fila < 0 or fila >= TAMANO or columna < 0 or columna >= TAMANO:
        return None

    en_hueco_derecha = (x - MARGEN) % PASO >= CELDA
    en_hueco_abajo = (y - MARGEN) % PASO >= CELDA

    if not en_hueco_derecha and not en_hueco_abajo:
        return ('mover', fila, columna)
    if en_hueco_abajo and not en_hueco_derecha and fila < TAMANO - 1:
        return ('h', fila, min(columna, TAMANO - 2))  # en la última columna el muro va una antes
    if en_hueco_derecha and not en_hueco_abajo and columna < TAMANO - 1:
        return ('v', min(fila, TAMANO - 2), columna)  # en la última fila el muro va una antes
    return None


def es_legal(estado, jugada):
    """¿Puede el humano hacer esta jugada?"""
    if jugada is None:
        return False
    if jugada[0] == 'mover':
        return (jugada[1], jugada[2]) in movimientos_peon(estado, HUMANO)
    return muro_valido(estado, jugada)


def dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos):
    """Dibuja todo: tablero, caminos, muros, peones y textos."""
    pantalla.fill(FONDO)
    quien_gana = ganador(estado)
    turno_humano = estado['turno'] == HUMANO and quien_gana is None

    # Casillas (la primera y la última fila, del color de quien tiene que llegar a ellas)
    for f in range(TAMANO):
        for c in range(TAMANO):
            color = CASILLA
            if f == 0:
                color = COLOR_META[HUMANO]
            if f == TAMANO - 1:
                color = COLOR_META[IA]
            pygame.draw.rect(pantalla, color, rect_casilla(f, c), border_radius=6)

    # Caminos más cortos que calcula A* (tecla C)
    if mostrar_caminos:
        for jugador in (HUMANO, IA):
            puntos = [rect_casilla(f, c).center for f, c in camino(estado, jugador)]
            if len(puntos) > 1:
                pygame.draw.lines(pantalla, COLOR_PEON[jugador], False, puntos, 4)

    # Puntos verdes donde puede moverse el humano
    if turno_humano:
        for f, c in movimientos_peon(estado, HUMANO):
            pygame.draw.circle(pantalla, VERDE, rect_casilla(f, c).center, 10)

    # Muros puestos
    for muro, jugador in estado['muros'].items():
        pygame.draw.rect(pantalla, COLOR_MURO[jugador], rect_muro(*muro), border_radius=4)

    # Muro que pondrías con el ratón: verde si se puede, gris si no
    jugada = raton_a_jugada(*pygame.mouse.get_pos())
    if turno_humano and jugada is not None and jugada[0] != 'mover':
        color = VERDE if muro_valido(estado, jugada) else GRIS
        pygame.draw.rect(pantalla, color, rect_muro(*jugada), border_radius=4)

    # Peones
    for jugador in (HUMANO, IA):
        centro = rect_casilla(*estado['peones'][jugador]).center
        pygame.draw.circle(pantalla, COLOR_PEON[jugador], centro, 20)
        pygame.draw.circle(pantalla, BLANCO, centro, 20, 2)  # borde blanco

    # Cartel del final: una franja negra con el ganador en grande
    if quien_gana is not None:
        centro_y = MARGEN + LADO_TABLERO // 2
        pygame.draw.rect(pantalla, NEGRO, (0, centro_y - 70, ANCHO, 130))
        if quien_gana == HUMANO:
            titulo = "¡HAS GANADO!"
        else:
            titulo = "¡GANA LA IA!"
        texto = fuente_grande.render(titulo, True, COLOR_MURO[quien_gana])
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, centro_y - 20)))
        texto = fuente.render("Pulsa R para jugar otra vez", True, BLANCO)
        pantalla.blit(texto, texto.get_rect(center=(ANCHO // 2, centro_y + 35)))

    # Textos de abajo
    if quien_gana is not None:
        mensaje = "Fin de la partida"
    elif turno_humano:
        mensaje = "Tu turno (azul): mueve o pon un muro en un hueco"
    else:
        mensaje = "La IA (rojo) está pensando..."
    muros = f"Muros  -  Tú: {estado['muros_restantes'][HUMANO]}/{MUROS_INICIALES}" \
            f"     IA: {estado['muros_restantes'][IA]}/{MUROS_INICIALES}"
    teclas = "C: caminos A*     R: reiniciar     ESC: salir"
    pantalla.blit(fuente.render(mensaje, True, BLANCO), (MARGEN, ANCHO - 10))
    pantalla.blit(fuente.render(muros, True, BLANCO), (MARGEN, ANCHO + 18))
    pantalla.blit(fuente.render(teclas, True, BLANCO), (MARGEN, ANCHO + 46))

    pygame.display.flip()  # enseña en la ventana todo lo dibujado


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
        # 1. Mirar qué ha hecho el jugador (teclado y ratón)
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                return
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return
                if evento.key == pygame.K_r:
                    estado = nueva_partida()
                if evento.key == pygame.K_c:
                    mostrar_caminos = not mostrar_caminos
            if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                jugada = raton_a_jugada(*evento.pos)
                if estado['turno'] == HUMANO and ganador(estado) is None and es_legal(estado, jugada):
                    estado = aplicar(estado, jugada)

        # 2. Dibujar (antes de que piense la IA, para que se vea "está pensando...")
        dibujar(pantalla, fuente, fuente_grande, estado, mostrar_caminos)

        # 3. Si le toca a la IA, juega
        if estado['turno'] == IA and ganador(estado) is None:
            estado = aplicar(estado, mejor_movimiento(estado))
            pygame.event.clear(pygame.MOUSEBUTTONDOWN)  # olvida los clics hechos mientras pensaba

        reloj.tick(30)  # como mucho 30 imágenes por segundo


if __name__ == "__main__":
    main()
