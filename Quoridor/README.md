# Quoridor con IA (Minimax + poda alfa-beta + A*)

Juego de **Quoridor** en Python con **pygame**: juegas tú (azul) contra una IA (rojo).

![Captura del juego](captura.png)

## Cómo jugar

```bash
pip install -r requirements.txt
python main.py
```

**Objetivo:** llevar tu peón a la fila del otro lado (tú empiezas abajo y vas arriba; la IA al revés).
Al terminar aparece en grande quién ha ganado.

En tu turno haces **una** de estas dos cosas:

- **Mover el peón** una casilla (arriba, abajo, izquierda o derecha): haz clic en una casilla marcada en verde.
  Si el rival está al lado, puedes saltar por encima; si detrás hay un muro, saltas en diagonal.
- **Poner un muro** (tienes 10): pasa el ratón por un hueco entre casillas y haz clic.
  La vista previa sale en verde si el muro es válido y en gris si no.
  Tus muros se pintan en azul y los de la IA en rojo.
  Un muro no puede solaparse con otro ni dejar a nadie sin camino hasta su meta.

| Tecla | Acción |
|-------|--------|
| `C`   | Mostrar u ocultar los caminos más cortos (A*) de cada jugador |
| `R`   | Reiniciar la partida |
| `ESC` | Salir |

## Estructura del código

| Archivo         | Qué hace |
|-----------------|----------|
| `main.py`       | Interfaz con pygame: dibuja el tablero y lee el ratón y el teclado. |
| `tablero.py`    | Reglas del juego: estado, movimientos de los peones (con saltos) y muros. |
| `a_estrella.py` | Algoritmo A* para el camino más corto de un peón hasta su meta. |
| `minimax.py`    | La IA: Minimax con poda alfa-beta. |

## Cómo piensa la IA

### A*

Busca el camino más corto desde un peón hasta su fila meta. Usa como heurística
el número de filas que faltan (nunca sobreestima, así que el camino encontrado es óptimo).
Se usa para:

1. **Validar muros**: un muro solo es legal si después los dos jugadores siguen teniendo camino.
2. **Evaluar posiciones**: lo que importa es cuántos pasos le faltan a cada uno.

### Minimax con poda alfa-beta

La IA simula las jugadas `PROFUNDIDAD` turnos hacia delante (por defecto 2) suponiendo que
tú también juegas lo mejor posible, y elige la jugada con mejor resultado.
La poda alfa-beta descarta ramas que no pueden cambiar la decisión, así que da el mismo
resultado que el minimax normal pero mucho más rápido.

**Función de evaluación** (positiva = buena para la IA):

```
10 * (tus_pasos_hasta_meta - pasos_de_la_IA) + (muros_IA - tus_muros)
```

**Jugadas que prueba:**

- Los movimientos del peón que lo acercan a su meta (si ninguno lo acerca, todos). Sin este filtro,
  la IA podía quedarse yendo y viniendo entre dos casillas por miedo a un muro que nunca llegaba.
- Solo los muros que cortan tu camino más corto (calculado con A*). Hay hasta ~130 muros posibles,
  pero los demás no te retrasan, y así el árbol de búsqueda es mucho más pequeño.

Para una IA más difícil, cambia `PROFUNDIDAD = 4` en `minimax.py` (tardará unos segundos por jugada).
