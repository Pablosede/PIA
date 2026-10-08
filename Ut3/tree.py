#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Tree:
    def __init__(self, data):
        self.children = []
        self.data = data

a = Tree("A")
b = Tree("B")
# c = Tree("C")
root = Tree("root")
root.children.append(a)
root.children.append(b)
# root.children.append(c)


a1=Tree("A1")
a2=Tree("A2")
root.children[0].children.append(a1)
root.children[0].children.append(a2)


b1=Tree("B1")
b2=Tree("B2")
root.children[1].children.append(b1)
root.children[1].children.append(b2)

'''
c1=Tree("C1")
c2=Tree("C2")
root.children[2].children.append(c1)
root.children[2].children.append(c2)
'''

# Hijos de A1 y A2:
'''
a11 = Tree("A11")
a12 = Tree("A12")
a21 = Tree("A21")
a1.children.append(a11)
a1.children.append(a12)
a2.children.append(a21)
'''


# Hijos de C2:
'''
c21 = Tree("C21")
c22 = Tree("C22")
c2.children.append(c21)
c2.children.append(c22)
'''

# Programar un algoritmo de exploración: Profundidad
'''
def recorrerP(arbol):
    print(arbol.data)
    for i in arbol.children:
        recorrerP(i)

recorrerP(root)
'''

# Programar un algoritmo de exploración: Amplitud

def recorrerA(arbol):
    for i in arbol.children:
        print(i.data)
    for i in arbol.children:
        recorrerA(i)

recorrerA(root)