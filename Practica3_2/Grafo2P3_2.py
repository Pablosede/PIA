import matplotlib.pyplot as plt
from fontTools.misc.cython import returns

from graph import Node, Graph


def crear_grafo():
    g = Graph()

    # Nodos con sus coordenadas (x, y)
    g.add_node(Node("A", (0, 1)))
    g.add_node(Node("B", (2, 2)))
    g.add_node(Node("C", (1, 0)))
    g.add_node(Node("D", (3, 0)))
    g.add_node(Node("E", (4, 1)))
    g.add_node(Node("F", (5, 0)))
    g.add_node(Node("G", (6, 2)))
    g.add_node(Node("H", (7, 1)))

    # Aristas con su peso (coste)
    g.add_edge("A", "B", 5)
    g.add_edge("A", "C", 2)
    g.add_edge("B", "C", 1)
    g.add_edge("B", "D", 2)
    g.add_edge("B", "E", 4)
    g.add_edge("C", "D", 7)
    g.add_edge("D", "E", 1)
    g.add_edge("E", "G", 12)
    g.add_edge("E", "F", 15)
    g.add_edge("F", "G", 1)

    return g


def mostrar_grafo(grafo):
    fig, ax = plt.subplots(figsize=(10, 5))

    # 1. Dibujar las aristas y su coste
    dibujadas = []  # para no dibujar dos veces la misma arista (A-B y B-A)
    for nodo in grafo.nodes:
        for vecino, peso in nodo.neighbors:
            if (vecino.value, nodo.value) in dibujadas:
                continue
            dibujadas.append((nodo.value, vecino.value))

            # Línea entre los dos nodos
            ax.plot([nodo.x, vecino.x], [nodo.y, vecino.y],
                    color="black", linewidth=1, zorder=1)

            # Coste en el punto medio de la arista
            medio_x = (nodo.x + vecino.x) / 2
            medio_y = (nodo.y + vecino.y) / 2
            ax.annotate(str(peso), xy=(medio_x, medio_y),
                        ha="center", va="center", fontsize=10,
                        bbox=dict(boxstyle="round,pad=0.2",
                                  fc="white", ec="none"),
                        zorder=2)

    # 2. Dibujar los nodos encima de las aristas
    for nodo in grafo.nodes:
        ax.scatter(nodo.x, nodo.y, s=900, c="white",
                   edgecolors="black", linewidths=1.5, zorder=3)
        ax.annotate(nodo.value, xy=(nodo.x, nodo.y),
                    ha="center", va="center", fontsize=12,
                    fontweight="bold", zorder=4)

    ax.set_title("Estructura del grafo")
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(-0.5, 2.5)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.show()


if __name__ == "__main__":
    grafo = crear_grafo()
    #mostrar_grafo(grafo)

    nodo_b = grafo.find_node("B")
    print(nodo_b.number_of_neighbors())
    for nodo in grafo.nodes:
        pass



