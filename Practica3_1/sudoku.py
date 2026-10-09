import numpy as np

# Ejercicio 1: Crea una función que cargue de un fichero de texto un tablero de sudoku representado
# de la siguiente forma:

def carga(nombre_fichero):
    matriz = np.loadtxt(nombre_fichero, delimiter=";", dtype=int)
    return matriz

sudoku = carga("matriz.txt")
print(sudoku)

# Ejercicio 2: Crea una función que determine si una fila de un sudoku tiene valores
# repetidos:

def esValidoFila(matriz, fila):
    for i in matriz:

        pass