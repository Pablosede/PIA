def combinaciones_suma(target, solucion_parcial, primera_opcion, soluciones):
    exito = False
    opciones = list(range(primera_opcion, target))
    i = 0
    while i < len(opciones):
        total = opciones[i] + sum(solucion_parcial)
        if total <= target:  # opcion aceptable?
            solucion_parcial.append(opciones[i])
            if total == target:  # es solución?
                soluciones.append(solucion_parcial.copy())
                exito = True
            else:
                exito = combinaciones_suma(target, solucion_parcial, primera_opcion, soluciones)

            solucion_parcial.pop()  # desanotar
        else:
            exito = False
            break;  # heurística: nos pasamos de cantidad, no hace falta seguir comprobando el resto de opciones
        i += 1

    return exito


target = 4
soluciones = []
solucion_parcial = []
combinaciones_suma(target, solucion_parcial, 1, soluciones)
print(soluciones)
print(len(soluciones))