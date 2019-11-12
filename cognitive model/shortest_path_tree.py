import networkx as nx
import matplotlib.pyplot as plt

#nodes = [('A', 'E', {'weight': 1}), ('A', 'C', {'weight': 3.8}), ('A', 'F', {'weight': 1.4}),
#         ('B', 'E', {'weight': 2}), ('B', 'C', {'weight': 3.4}), ('B', 'F', {'weight': 2.4}),
#         ('F', 'E', {'weight': 1}), ('F', 'C', {'weight': 3.4})]

nodes = [#('cutting_board', 'silverware', {'weight': 1}), ('cutting_board', 'table_c', {'weight': 3.8}), ('cutting_board', 'start', {'weight': 1.4}),
        ('tray', 'silverware', {'weight': 1}), ('tray', 'table_c', {'weight': 3.8}), ('tray', 'start', {'weight': 1.4}), ('tray', 'plate', {'weight': 3}), ('tray', 'cup', {'weight': 3}),
        ('napkin', 'silverware', {'weight': 1}), ('napkin', 'table_c', {'weight': 3.8}), ('napkin', 'start', {'weight': 1.4}), ('napkin', 'plate', {'weight': 3}), ('napkin', 'cup', {'weight': 3}),
        ('plate', 'silverware', {'weight': 2}), ('plate', 'table_c', {'weight': 3.4}), ('plate', 'start', {'weight': 2.4}),
        ('cup', 'silverware', {'weight': 2}), ('cup', 'table_c', {'weight': 3.4}), ('cup', 'start', {'weight': 2.4}),
        ('start', 'silverware', {'weight': 1}), ('start', 'table_c', {'weight': 2.4}),
        ('napkin', 'tray', {'weight': 0}), ('plate', 'cup', {'weight': 0})]

graph = nx.Graph()
graph.add_edges_from(nodes)

print(list(nx.all_simple_paths(graph, 'start', 'table_c')))

nx.draw_networkx(graph, with_label = True)
plt.show()