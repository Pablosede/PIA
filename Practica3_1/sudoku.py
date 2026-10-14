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
    filasVistas=[]
    for i in matriz[fila]:
        if i ==0:
            continue
        if i >0 & i<=9:
            if i in filasVistas:
                return False
        filasVistas.append(i)
    return True
print(esValidoFila(sudoku, 0))

def esValidoColumna(matriz, columna):
    columnasVistas=[]
    for i in matriz[:,columna]:
        if i ==0:
            continue
        if i >0 & i<=9:
            if i in columnasVistas:
                return False
        columnasVistas.append(i)
    return True
print(esValidoColumna(sudoku, 0))

def esValidoCuadro(matriz, fila, columna):
    cuadroValido=[]
    for i in range(fila, fila+3):
        for j in range(columna, columna+3):
            if i ==0:
                continue
            if esValidoFila(matriz, fila):
                if i in cuadroValido:
                    return False
            cuadroValido.append(i)
            if j ==0:
                continue
            if esValidoColumna(matriz, columna):
                if j in cuadroValido:
                    return False
            cuadroValido.append(j)
    return True
print(esValidoCuadro(sudoku, 0, 0))
