
from graph import Graph, Node
from a_star import AStar

def run():
    # Create graph
    graph = Graph()
    # Add vertices
    graph.add_node(Node('S', (1 ,1)))
    graph.add_node(Node('B', (1 ,2)))
    graph.add_node(Node('C', (1 ,4)))
    graph.add_node(Node('D', (2 ,1)))
    graph.add_node(Node('E', (2 ,2)))
    graph.add_node(Node('F', (2 ,3)))
    graph.add_node(Node('G', (2 ,4)))
    graph.add_node(Node('H', (3 ,1)))
    graph.add_node(Node('I', (3 ,4)))
    graph.add_node(Node('J', (4 ,1)))
    graph.add_node(Node('K', (4 ,2)))
    graph.add_node(Node('T', (4 ,3)))
    graph.add_node(Node('L', (4 ,4)))

    # Add edges
    graph.add_edge('S', 'B', 4)
    graph.add_edge('S', 'D', 5)
    graph.add_edge('B', 'E', 1)
    graph.add_edge('C', 'G', 1)
    graph.add_edge('D', 'E', 2)
    graph.add_edge('D', 'H', 3)
    graph.add_edge('E', 'F', 6)
    graph.add_edge('F', 'G', 4)
    graph.add_edge('G', 'I', 3)
    graph.add_edge('H', 'J', 1)
    graph.add_edge('I', 'L', 4)
    graph.add_edge('J', 'K', 6)
    graph.add_edge('K', 'T', 2)
    graph.add_edge('T', 'L', 3)

    # Execute the algorithm
    alg = AStar(graph, "S", "T")
    path, path_length = alg.search()
    print(" -> ".join(path))
    print(f"Length of the path: {path_length}")

    import matplotlib.pyplot as plt

    plt.title("Ruta al destino")
    plt.ylim([0 ,5])
    plt.xlim([0 ,5])
    x=[]
    y=[]

    colores=[]
    for i in graph.nodes:
        x.append(i.x)
        y.append(i.y)

        plt.annotate(i.value, (i.x,i.y) ,xytext=(i.x+0.1 , i.y+ 0.2 ) )
        colores.append("green" if i.value in path else "#a0a0a0")
        vecinosx=[]
        vecinosy=[]
        for j in i.neighbors:
            vecinosx.extend([j[0].x,i.x] )
            vecinosy.extend([j[0].y,i.y] )
        plt.plot(vecinosx,vecinosy,"*-k ")

    caminox=[]
    caminoy=[]
    for indice,i in enumerate(path):
        nodo=graph.find_node(i)
        caminox.append(nodo.x)
        caminoy.append(nodo.y)
        plt.annotate(indice,(nodo.x,nodo.y),c="b lue",xytext=(nodo.x+0.1 , nodo .y-0.3 ) ,fontsize=8)



    plt.scatter( x=x, y=y,c=colores,s=100)
    plt.plot(caminox,caminoy,"* --",color="#66ff66")



    plt.show()


if __name__ == '__main__':
    run()

# S -> D -> H -> J -> K -> T
# Length of the path: 17

'''
import networkx as nx
from matplotlib import pyplot as plt

g = nx.Graph()
g.add_node('S', pos=(1, 1))
g.add_node('D', pos=(2, 1))
g.add_node('H', pos=(3, 1))
g.add_node('J', pos=(4, 1))
g.add_node('B', pos=(1, 2))
g.add_node('E', pos=(2, 2))
g.add_node('K', pos=(4, 2))
g.add_node('F', pos=(2, 3))
g.add_node('T', pos=(4, 3))
g.add_node('C', pos=(1, 4))
g.add_node('G', pos=(2, 4))
g.add_node('I', pos=(3, 4))
g.add_node('L', pos=(4, 4))

g.add_edge('S', 'B', lenght=4)
g.add_edge('S', 'D', lenght=5)
g.add_edge('B', 'E', lenght=1)
g.add_edge('D', 'E', lenght=2)
g.add_edge('E', 'F', lenght=6)
g.add_edge('F', 'G', lenght=4)
g.add_edge('G', 'C', lenght=1)
g.add_edge('G', 'I', lenght=3)
g.add_edge('I', 'L', lenght=4)
g.add_edge('L', 'T', lenght=3)
g.add_edge('T', 'K', lenght=2)
g.add_edge('K', 'J', lenght=6)
g.add_edge('J', 'H', lenght=1)
g.add_edge('H', 'D', lenght=3)

labels = nx.get_edge_attributes(g,'lenght')
pos=nx.get_node_attributes(g,'pos')
print("etiquetas",labels)
print("Posiciones",pos)
nx.draw_networkx(g, pos,with_labels=True)
nx.draw_networkx_edge_labels(g, pos,edge_labels=labels)
plt.show()
'''





'''
import matplotlib.pyplot as plt
from Ut3 import graph
from Ut3.graph import Node

miGraph = graph.Graph()
miNode = [Node("A", (1,2)), Node("B", (2,3)),
          Node("C", (3,4)), Node("D", (4,2)),
          Node("E", (2,1)), Node("F", (3,3)),
          Node("G", (3,1))]


for nodos in miNode:
    miGraph.add_node(nodos)

miGraph.add_edge("A", "B", 2)
miGraph.add_edge("A", "E", 1)
miGraph.add_edge("B", "E", 3)
miGraph.add_edge("E", "G", 6)
miGraph.add_edge("C", "F", 2)
miGraph.add_edge("F", "G", 5)
miGraph.add_edge("F", "D", 1)
miGraph.add_edge("D", "G", 4)

print(miGraph)

# 6. Dibujar el grafo
fig, ax = plt.subplots()

# Aristas (cada una se guarda en los dos nodos, así que evitamos dibujarla dos veces)
dibujadas = set()
for nodo in miGraph.nodes:
    for vecino, peso in nodo.neighbors:
        arista = tuple(sorted((nodo.value, vecino.value)))
        if arista in dibujadas:
            continue
        dibujadas.add(arista)
        ax.plot([nodo.x, vecino.x], [nodo.y, vecino.y], color="black", linewidth=1, zorder=1)
        # Peso en el punto medio de la arista
        mx, my = (nodo.x + vecino.x) / 2, (nodo.y + vecino.y) / 2
        ax.text(mx, my, str(peso), ha="center", va="center", fontsize=9,
                bbox=dict(facecolor="white", edgecolor="none", pad=1), zorder=2)

# Nodos
for nodo in miGraph.nodes:
    ax.scatter(nodo.x, nodo.y, s=250, color="tab:blue", zorder=3)
    ax.text(nodo.x, nodo.y, nodo.value, ha="center", va="center", fontsize=9, zorder=4)

plt.show()
'''
