import pandas as pd

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


def dijkstra(graph, source):
    """
    Implements Dijkstra's single source shortest path (SSSP)
    Arguments: graph object, source node"""
    q = set()
    dist = {}
    prev = {}

    for v in graph.nodes:       # initialization
        dist[v] = float('inf')      # unknown distance from source to v
        prev[v] = float('inf')      # previous node in optimal path from source
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
    while previous_node != float('inf'):
        route.append(previous_node.label)
        temp = previous_node
        previous_node = prev[temp]

    route.reverse()
    return route

# Create instance of Graph
graph = Graph()

# Prepare data
# Read data from csv
raw = pd.read_csv('tum_edges_list.csv', header=0, usecols=[0,1,2,3])

# No constraints for how many objects at once
#data = raw

# Add constraint: Only 1 object at once
data = raw.loc[raw['obj_at_once'] == 1]

# Reset index
data = data.reset_index(drop=True)

# Create sorted set of nodes from to_nodes and from_nodes
nodes = sorted(pd.unique(data[['from_node', 'to_node']].values.ravel()))

# Create nodes from set
for x in range(0, len(nodes)):
    globals()[nodes[x]] = Node(nodes[x]) # create node as global variable
    graph.add_node(globals()[nodes[x]])  # add node to graph

# Add edge for row in csv -> from_node, to_node, weight
for row in range(0, len(data)):
    to_node = globals()[data['to_node'][row]] #
    from_node = globals()[data['from_node'][row]]
    graph.add_edge(from_node, to_node, data['weight'][row])

# Run dijkstra on data
dist, prev = dijkstra(graph, table_empty)

print("The quickest path from {} to {} is [{}] with a distance of {}".format(
    table_empty.label,
    pcstn.label,
    " -> ".join(to_array(prev, pcstn)),
    str(round(dist[pcstn], 1))
    )
)
