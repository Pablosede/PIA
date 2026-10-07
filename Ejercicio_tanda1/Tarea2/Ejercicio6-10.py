#Ejercicio 6: Con la función input(), indícale al usuario que introduzca su nombre y
# guárdalo en la variable llamada nombre

nombre=input("Introduzca su nombre: ")
print("Hola "+nombre)

#Ejercicio 7: Con la función input(), indícale al usuario que introduzca su apellido y
# guárdalo en la variable llamada apellido

apellido=input("Introduzca su apellido: ")
print("Hola "+nombre, apellido)

#Ejercicio 8: Con la función input(), indícale al usuario que introduzca su edad y
# guárdala en la variable llamada edad. ¡Ojo con el tipo de dato!

edad=int(input("Introduzca su edad: "))
print(nombre, apellido,  "tiene", edad)

#Ejercicio 9: Con la función input(), indícale al usuario que introduzca la ciudad en la que vive y
# guárdala en la variable llamada ciudad.

ciudad=input("Introduzca su ciudad: ")
print(nombre, apellido, "vive", ciudad)

#Ejercicio 10 todos los ejs juntos

print("Su nombre es", nombre, apellido+",","tiene",edad, "y actualmente vive en", ciudad)
