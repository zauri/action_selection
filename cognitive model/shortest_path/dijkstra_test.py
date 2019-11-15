class Node:
    def __init__(self, label):
        self.label = label

class Edge:
    def __init__(self, to_node, length):
        self.to_node = to_node
        self.length = length


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = dict()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, from_node, to_node, length):
        edge = Edge(to_node, length)
        if from_node.label in self.edges:
            from_node_edges = self.edges[from_node.label]
        else:
            self.edges[from_node.label] = dict()
            from_node_edges = self.edges[from_node.label]
        from_node_edges[to_node.label] = edge


def min_dist(q, dist):
    """
    Returns the node with the smallest distance in q.
    Implemented to keep the main algorithm clean.
    """
    min_node = None
    for node in q:
        if min_node == None:
            min_node = node
        elif dist[node] < dist[min_node]:
            min_node = node

    return min_node

INFINITY = float('inf')

def dijkstra(graph, source):
    q = set()
    dist = {}
    prev = {}

    for v in graph.nodes:       # initialization
        dist[v] = INFINITY      # unknown distance from source to v
        prev[v] = INFINITY      # previous node in optimal path from source
        q.add(v)                # all nodes initially in q (unvisited nodes)

    # distance from source to source
    dist[source] = 0

    while q:
        # node with the least distance selected first
        u = min_dist(q, dist)

        q.remove(u)

        if u.label in graph.edges:
            for _, v in graph.edges[u.label].items():
                alt = dist[u] + v.length
                if alt < dist[v.to_node]:
                    # a shorter path to v has been found
                    dist[v.to_node] = alt
                    prev[v.to_node] = u

    return dist, prev


def to_array(prev, from_node):
    """Creates an ordered list of labels as a route."""
    previous_node = prev[from_node]
    route = [from_node.label]
    while previous_node != INFINITY:
        route.append(previous_node.label)
        temp = previous_node
        previous_node = prev[temp]

    route.reverse()
    return route


graph = Graph()

root = Node('table_empty')
graph.add_node(root)
cup = Node('cup')
graph.add_node(cup)
plate = Node('plate')
graph.add_node(plate)
silverware = Node('silverware')
graph.add_node(silverware)

pc = Node('plate, cup')
graph.add_node(pc)
ps = Node('plate, silverware')
graph.add_node(ps)
cs = Node('cup, silverware')
graph.add_node(cs)

target = Node('plate, cup, silverware')
graph.add_node(target)

graph.add_edge(root, cup, 5.8)
graph.add_edge(root, plate, 5.8)
graph.add_edge(root, silverware, 4.4)
graph.add_edge(root, pc, 5.8)
graph.add_edge(root, ps, 6.8)
graph.add_edge(root, cs, 6.8)
graph.add_edge(plate, pc, 6.8)
graph.add_edge(plate, ps, 6.8)
graph.add_edge(cup, pc, 6.8)
graph.add_edge(cup, cs, 6.8)
graph.add_edge(silverware, cs, 6.8)
graph.add_edge(silverware, ps, 6.8)
graph.add_edge(pc, target, 6.8)
graph.add_edge(ps, target, 6.8)
graph.add_edge(cs, target, 6.8)

dist, prev = dijkstra(graph, root)

print("The quickest path from {} to {} is [{}] with a distance of {}".format(
    root.label,
    target.label,
    " -> ".join(to_array(prev, target)),
    str(dist[target])
    )
)