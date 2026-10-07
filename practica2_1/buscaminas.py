import numpy as np
# Apartado a:
def generarMatriz(filas, columnas):
    matriz = np.zeros([filas,columnas])

    minas=0

    while minas<11:
        filasR = np.random.randint(1,8)
        colunasR = np.random.randint(1,8)
        matriz[filasR][colunasR] = -1
        minas+=1
    return matriz

#Apartado b:
def contarMinas(matriz):

    for fila in range(matriz.shape[0]):
        for columna in range(matriz.shape[1]):
            minas=0
            for i in range (fila-1,fila+2):
                for j in range (columna-1,columna+2):
                    if i< matriz.shape[0] and j<matriz.shape[1] and matriz[i, j]==-1 and i>=0 and j>=0:
                        minas+=1
            if matriz[fila][columna]!=-1:
                matriz[fila][columna]=minas
    return matriz



#Apartado c:
def descubrir(matriz, visible, i, j):
    if i < 0 or j<0 or i>=matriz.shape[0] or j>=matriz.shape[1]:
        return
    if visible[i, j]:
        return
    visible[i, j] = True

    if matriz[i-1][j-1]!=-1:
       for k in (-1,0,1):
           for l in (-1,0,1):
               descubrir(matriz, visible, i+k, j+l)

def mostrar(matriz, visible):
    for i in range(matriz.shape[0]):
        fila= ""
        for j in range(matriz.shape[1]):
            if not visible[i, j]:
                fila+="?"
            elif matriz[i, j]==-1:
                fila+="*"
            else:
                fila+=str(matriz[i, j])+" "
        print(fila)

matriz=contarMinas(generarMatriz(8,8))
visible=np.zeros(matriz.shape)

i, j = 0, 0
if matriz[i, j] == -1:
    print("¡Mina! Fin del juego")
else:
    descubrir(matriz, visible, i, j)

print(matriz)
print()
mostrar(matriz, visible)