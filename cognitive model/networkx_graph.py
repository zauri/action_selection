import networkx as nx
import matplotlib.pyplot as plt
import numpy as np


edges = [#('cutting_board', 'silverware', {'weight': 1}), ('cutting_board', 'table_c', {'weight': 3.8}), ('cutting_board', 'start', {'weight': 1.4}),
        ('tray', 'silverware', {'weight': 1}), ('tray', 'table_c', {'weight': 3.8}), ('tray', 'start', {'weight': 1.4}), ('tray', 'plate', {'weight': 3}), ('tray', 'cup', {'weight': 3}),
        ('napkin', 'silverware', {'weight': 1}), ('napkin', 'table_c', {'weight': 3.8}), ('napkin', 'start', {'weight': 1.4}), ('napkin', 'plate', {'weight': 3}), ('napkin', 'cup', {'weight': 3}),
        ('plate', 'silverware', {'weight': 2}), ('plate', 'table_c', {'weight': 3.4}), ('plate', 'start', {'weight': 2.4}),
        ('cup', 'silverware', {'weight': 2}), ('cup', 'table_c', {'weight': 3.4}), ('cup', 'start', {'weight': 2.4}),
        ('start', 'silverware', {'weight': 1}), ('start', 'table_c', {'weight': 2.4}),
        ('napkin', 'tray', {'weight': 0}), ('plate', 'cup', {'weight': 0})]

nodes = [('plate', {'pos': (1,4)}), ('cup', {'pos': (1,4)}), ('silverware', {'pos': (1,2)}),
        ('tray', {'pos': (1,1)}), ('napkin', {'pos': (1,1)}),
         ('start', {'pos': (2,2)}), ('table_c', {'pos': (4,3)})]

graph = nx.Graph()
graph.add_edges_from(edges)

# print list of all possible direct paths
#print(list(nx.all_simple_paths(graph, 'start', 'table_c')))

#nx.draw_networkx(graph, with_label = True)
#plt.show()


graph2 = nx.DiGraph()
graph2.add_nodes_from(nodes)

#graph2.add_weighted_edges_from([('plate', 'cup', 0), ('plate', 'silverware', 2),
#                               ('plate', 'tray', 3), ('plate', 'napkin', 3)])

#graph2.add_edge('plate', 'cup', np.linalg.norm(nodes[0][1],nodes[1][1]))

pos = nx.get_node_attributes(graph2, 'pos')
nx.draw(graph2, with_labels=True)
plt.show()
