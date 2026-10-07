mLista =[82, 14, 27, 17, 72, 11, 24]

pivote = 17 # elemento central

def quickSort (lista, inicio, fin):
    if len(lista)==0:
        return []

    pivote = lista[(inicio+fin)//2]

    left = []
    right = []

    for i in range(inicio, fin):
        if lista[i] < pivote:
            left.append(lista[i])
        if lista[i] > pivote:
            right.append(lista[i])
    return quickSort(left, 0, len(left)) + [pivote] + quickSort(right, 0, len(right))

print(quickSort(mLista, 0, len(mLista)))