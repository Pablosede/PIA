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
        if i in columnasVistas:
            return False
        columnasVistas.append(i)
    return True
print(esValidoColumna(sudoku, 0))

def esValidoCuadro(matriz, fila, columna):
    inicioFila = (fila // 3) * 3
    inicioColumna = (columna // 3) * 3
    cuadroValido=[]
    for i in range(inicioFila, inicioFila+3):
        for j in range(inicioColumna, inicioColumna+3):
            valor = matriz[i][j]
            if valor ==0:
                continue
            if valor in cuadroValido:
                return False
            cuadroValido.append(valor)
    return True
print(esValidoCuadro(sudoku, 0, 0))
