miLista = [1,8,14,25,42,44,49,68,70,82,91]
def busquedaBinaria(lista, inicio, fin, elemento, contador = 0):
    contador += 1
    # caso base 1
    if inicio > fin:
        return -1, contador

    # caso base 2
    medio = (inicio+fin)//2
    if lista[medio]==elemento:
        return medio, contador
    if lista[medio]>elemento:
        return busquedaBinaria(lista, inicio, medio-1,elemento, contador)
    else:
        return busquedaBinaria(lista, medio+1, fin, elemento, contador)

pos = busquedaBinaria(miLista, 0, len(miLista)-1, 25)
print(pos)