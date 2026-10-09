def suma_peso(mochila):
    suma=0
    for peso,valor in mochila:
        suma+=peso
    return suma

def suma_valor(mochila):
    suma=0
    for peso,valor in mochila:
        suma+=valor
    return suma

def es_opcion_aceptable(mochila,objeto,peso_max):
    peso, valor = objeto
    return suma_peso(mochila) + peso <= peso_max
    """
    :param mochila:
    :param objeto: tupla peso,valor
    :param peso_max:
    :return:
    """

def compara_mochila(mochila1, mochila2):
    return suma_valor(mochila1) < suma_valor(mochila2)
    """
    TODO
    :param mochila1:
    :param mochila2:
    :return: True si mochila1 tiene más valor que mochila2
    """

def copia_mochila(mochila_final, mochila):
    mochila_final.clear()
    for i in mochila:
        x,y = i
        mochila_final.append((x,y))
    return
    """
    TODO
    copia en mochila_final el contenido de mochila:
        vacía mochila_final y copia todos los elementos de mochila

    :param mochila_final:
    :param mochila:
    :return: None
    """

# backtracking
def optimiza_mochila(mochila,mochila_optima,items,peso_max):
    for i in range(len(items)):
        objeto = items[i]
        if es_opcion_aceptable(mochila,mochila,peso_max):
            # Anotar (MOVER) un objeto a la mochila
            mochila.append(objeto)
            items.pop(i)
            if compara_mochila(mochila,mochila_optima):
                # Devuelve que mochila es mejor
                copia_mochila(mochila_optima,mochila)
            optimiza_mochila(mochila,mochila_optima,items,peso_max)
            # Desanotar: Quitar el objeto que añadí y lo meto en la lista de items
            mochila.pop()
            items.append(objeto)
            items.append(objeto)

mochila=[] # mochila provisional que vamos generando en cada estado nuevo
mochila_optima=[] # mochila optima
items=[(12,4),(2,2),(1,2),(4,10),(1,1)]
peso_max=15
optimiza_mochila(mochila,mochila_optima,items,peso_max)
print(mochila_optima)
print("Valor de la mochila: " , suma_valor(mochila_optima))
print("Peso de la mochila: " , suma_peso(mochila_optima))
