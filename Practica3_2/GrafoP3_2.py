import networkx as nx
from matplotlib import pyplot as plt

g=nx.Graph()
g.add_nodes_from('A',pos=(0,1))
g.add_nodes_from('B',pos=(2,2))
g.add_nodes_from('C',pos=(1,0))
g.add_nodes_from('D',pos=(3,0))
g.add_nodes_from('E',pos=(4,1))
g.add_nodes_from('F',pos=(5,0))
g.add_nodes_from('G',pos=(6,2))
g.add_nodes_from('H',pos=(7,1))

g.add_edge('A','B', lenght=5)
g.add_edge('A','C', lenght=2)
g.add_edge('B','C', lenght=1)
g.add_edge('B','D', lenght=2)
g.add_edge('B','E', lenght=4)
g.add_edge('C','D', lenght=7)
g.add_edge('D','E', lenght=1)
g.add_edge('E','F', lenght=15)
g.add_edge('E','G', lenght=12)
g.add_edge('F','G', lenght=1)

labels = nx.get_edge_attributes(g,'lenght')
pos=nx.get_node_attributes(g,'pos')
print("etiquetas",labels)
print("Posiciones",pos)
nx.draw_networkx(g, pos,with_labels=True)
nx.draw_networkx_edge_labels(g, pos,edge_labels=labels)
plt.show()

