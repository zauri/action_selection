from collections import defaultdict


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = defaultdict(list)
        self.distances = {}

    def add_node(self, value):
        self.nodes.add(value)

    def add_edge(self, from_node, to_node, distance):
        self.edges[from_node].append(to_node)
        #self.edges[to_node].append(from_node)
        self.distances[(from_node, to_node)] = distance


def dijsktra(graph, initial):
    visited = {initial: 0}
    #path = {}
    path = defaultdict(list)

    nodes = set(graph.nodes)

    while nodes:
        min_node = None
        for node in nodes:
            if node in visited:
                if min_node is None:
                    min_node = node
                elif visited[node] < visited[min_node]:
                    min_node = node

        if min_node is None:
            break

        nodes.remove(min_node)
        current_weight = visited[min_node]

        for edge in graph.edges[min_node]:
            weight = current_weight + graph.distances[(min_node, edge)]
            if edge not in visited or weight < visited[edge]:
                visited[edge] = weight
                path[edge].append(min_node)

    return path


nodes = ['plate', 'cup', 'silverware', 'plate, cup', 'plate, silverware', 'cup, silverware', 'plate, cup, silverware',
         'table_empty']
edges = [['table_empty', 'plate', 5.8],
         ['table_empty', 'cup', 5.8],
         ['table_empty', 'silverware', 4.4],
         ['table_empty', 'plate, cup', 5.8],
         ['table_empty', 'plate, silverware', 6.8],
         ['table_empty', 'cup, silverware', 6.8],
         ['plate', 'plate, cup', 6.8],
         ['plate', 'plate, silverware', 6.8],
         ['cup', 'plate, cup', 6.8],
         ['cup', 'cup, silverware', 6.8],
         ['silverware', 'plate, silverware', 6.8],
         ['silverware', 'cup, silverware', 6.8],
         ['plate, cup', 'plate, cup, silverware', 6.8],
         ['plate, silverware', 'plate, cup, silverware', 6.8],
         ['cup, silverware', 'plate, cup, silverware', 6.8]
         ]

graph = Graph()

for i in range(0, len(nodes)-1):
    graph.add_node(nodes[i])

for i in range(0, len(edges)-1):
    graph.add_edge(edges[i][0], edges[i][1], edges[i][2])

print(dijsktra(graph, 'table_empty')['plate'])

