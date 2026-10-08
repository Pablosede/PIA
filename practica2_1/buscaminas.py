import numpy as np
# Apartado a:
def generarMatriz(filas, columnas):
    matriz = np.zeros([filas,columnas])

    minas=0

    while minas<10:
        filasR = np.random.randint(0,filas)
        colunasR = np.random.randint(0,columnas)
        if matriz[filasR][colunasR]!=-1:
            matriz[filasR][colunasR] = -1
            minas+=1
    return matriz
matriz=generarMatriz(8,8)

#Apartado b:
def contarMinas(matriz):

    for fila in range(matriz.shape[0]):
        for columna in range(matriz.shape[1]):
            minas=0
            for i in range (fila-1,fila+2):
                for j in range (columna-1,columna+2):
                    if i< matriz.shape[0] and j<matriz.shape[1] and matriz[i][j]==-1 and i>=0 and j>=0:
                        minas+=1
            if matriz[fila][columna]!=-1:
                matriz[fila][columna]=minas
    return matriz

#Apartado c:
def descubrir(matriz, filas, columnas):
    if filas >= matriz.shape[0] or columnas >= matriz.shape[1] or filas<0 or columnas<0:
        return
    if matriz[filas][columnas]<0:
        return
    if matriz[filas][columnas]>0:
        matriz[filas][columnas]=-2
        return
    matriz[filas][columnas]=-2
    for i in range (filas-1,filas+2):
        for j in range (columnas-1,columnas+2):
            descubrir(matriz,i,j)

contarMinas(matriz)
descubrir(matriz,0,0)
print(matriz)