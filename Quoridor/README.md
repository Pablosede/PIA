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
  El muro empieza en la casilla que tiene encima (o a la izquierda) el ratón y ocupa 2 casillas.
  Antes de hacer clic se ve en verde si se puede poner y en gris si no.
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
| `main.py`       | La ventana con pygame: dibuja el tablero y lee el ratón y el teclado. |
| `tablero.py`    | Las reglas: cómo se mueven los peones (con saltos) y dónde caben los muros. |
| `a_estrella.py` | El algoritmo **A\***: el camino más corto de un peón hasta su meta. |
| `minimax.py`    | La IA: **Minimax con poda alfa-beta**. |

La partida se guarda en un diccionario (el "estado"). Cada jugada crea uno nuevo con `aplicar()`.

```python
{'peones': [(8, 4), (0, 4)],         # casilla de cada jugador: [tú, IA]
 'muros': {('h', 3, 4): 0},          # muros puestos -> quién lo puso (0 = tú, 1 = IA)
 'muros_restantes': [10, 10],
 'turno': 0,                         # a quién le toca: 0 = tú, 1 = IA
 'caminos': {}}                      # caminos de A* ya calculados en este estado
```

## Cómo piensa la IA

### A*

Busca el camino más corto desde un peón hasta su fila meta:

1. Hay una lista de casillas "por visitar". Al principio solo está la del peón.
2. Cada vez elige la más prometedora: la de menor `f = g + h`, donde `g` son los pasos dados
   y `h` las filas que faltan hasta la meta.
3. Si esa casilla está en la meta, ya tiene el camino. Si no, apunta sus vecinas y repite.

Se usa para dos cosas:

1. **Saber si un muro es válido**: no se puede dejar a nadie sin camino hasta su meta.
2. **Puntuar la partida**: lo que importa es cuántos pasos le faltan a cada uno.

Cada camino se calcula una sola vez por estado: `camino()` lo apunta en `estado['caminos']`
y las siguientes veces lo lee de ahí.

### Minimax con poda alfa-beta

La IA prueba sus jugadas, tus respuestas, las suyas... hasta 4 turnos hacia delante
(`PROFUNDIDAD`), suponiendo que tú también juegas lo mejor posible, y elige la mejor.
La poda alfa-beta deja de mirar las jugadas que seguro no se van a elegir: da el mismo
resultado pero mucho más rápido.

**Puntuación** (positiva = va ganando la IA):

```
10 * (tus_pasos_hasta_meta - pasos_de_la_IA) + 5 * (muros_IA - tus_muros)
```

Que cada muro guardado valga 5 hace que la IA no los gaste pronto y los guarde para cuando
estás a punto de llegar. En las pruebas fue el valor con el que más partidas ganaba.

**Jugadas que prueba** (no todas, solo las útiles):

- Mover el peón a casillas que lo acercan a su meta (si ninguna lo acerca, todas). Sin esto, la IA
  a veces se quedaba yendo y viniendo entre dos casillas.
- Poner solo los muros que cortan tu camino más corto. Hay unos 130 muros posibles, pero los demás
  no te retrasan y solo harían la búsqueda más lenta. Se prueban empezando por los que tienes más
  cerca: suelen ser los mejores, y probar primero lo mejor hace que la poda alfa-beta corte mucho antes.

Cada muro se comprueba (que no encierre a nadie) justo antes de probarlo, dentro de `minimax()`:
así, si la poda corta antes, no se pierde tiempo comprobándolo.

### Dificultad

Tarda menos de una décima de segundo por jugada de media (medio segundo en las más complicadas).
Para hacerla más fácil, pon `PROFUNDIDAD = 2` en `minimax.py`.
