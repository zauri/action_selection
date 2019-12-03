import pandas as pd
from scipy.spatial import distance

coordinates = {'c': (1,4),
              'n': (1,1),
              'p': (1,4),
              's': (1,2),
              't': (1,1),
              'start': (2,2),
              'table': (4,3)}


def prepare_data(objects_at_once=2):
    """
    Reads data from csv and drops node connections (edges) not meeting the specified constraint
    (e.g. taking more than one object at once).
    """

    # Read data from csv
    raw = pd.read_csv('tum_edges_list.csv', header=0, usecols=[0, 1, 2, 3, 4])

    # No constraints for how many objects at once
    if objects_at_once == 2:
        data = raw
    elif objects_at_once == 1:
        # Add constraint: Only 1 object at once
        data = raw.loc[raw['obj_at_once'] == 1]

    # Reset index
    data = data.reset_index(drop=True)

    return data


def calculate_distances(data):
    """
    Calculates euclidean distance between nodes of graph
    """
    for row in range(0, len(data)):
        # Distance = start -> obj 1 -> table
        if data['from_node'][row] == 'table_empty' and len(data['to_node'][row]) == 1:
            data.loc[row, 'dist'] = (distance.euclidean(
                coordinates['start'],
                coordinates[data['to_node'][row]]) +
                                     distance.euclidean(
                                         coordinates[data['to_node'][row]],
                                         coordinates['table'])
                                     )

        # Distance = start -> obj 1 -> obj 2 -> table
        elif data['from_node'][row] == 'table_empty' and len(data['to_node'][row]) != 1:
            data.loc[row, 'dist'] = (distance.euclidean(
                coordinates['start'],
                coordinates[data['to_node'][row][0]]) +
                                     distance.euclidean(
                                         coordinates[data['to_node'][row][0]],
                                         coordinates[data['to_node'][row][1]]) +
                                     distance.euclidean(
                                         coordinates[data['to_node'][row][1]],
                                         coordinates['table'])
                                     )
        # Distance = table -> obj 1 -> (obj 2) -> table
        else:
            # Get difference between sequences (from_node, to_node)
            diff = [x for x in data['to_node'][row] if x not in data['from_node'][row]]

            if len(diff) == 1:
                data.loc[row, 'dist'] = distance.euclidean(
                    coordinates['table'],
                    coordinates[diff[0]]) * 2

            elif len(diff) == 2:
                data.loc[row, 'dist'] = (distance.euclidean(
                    coordinates['table'],
                    coordinates[diff[0]]) +
                                         distance.euclidean(
                                             coordinates[diff[0]],
                                             coordinates[diff[1]]) +
                                         distance.euclidean(
                                             coordinates[diff[1]],
                                             coordinates['table'])
                                         )
    return data


def calculate_edge_weights(data):
    """
    Resets weights according to chosen weight function
    """
    for row in range(0, len(data)):
        if 'c' in data['to_node'][row]:
            data.loc[row, 'weight_new'] = (data['dist'][row] ** 1.0) * 1.2
        elif 'p' in data['to_node'][row]:
            data.loc[row, 'weight_new'] = (data['dist'][row] ** 0.9) * 1.2
        elif 's' in data['to_node'][row]:
            data.loc[row, 'weight_new'] = (data['dist'][row] ** 1.0) * 1.2
        elif 'n' in data['to_node'][row]:
            data.loc[row, 'weight_new'] = (data['dist'][row] ** 0.95) * 1.0
        elif 't' in data['to_node'][row]:
            data.loc[row, 'weight_new'] = (data['dist'][row] ** 0.9) * 1.0
        else:
            data.loc[row, 'weight_new'] = data['dist'][row]

    for row in range(0, len(data)):
        data.loc[row, 'weight_rounded'] = round(data['weight_new'][row], 2)

    return data


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


def create_nodes_edges(graph, data):
    """
    Creates nodes and edges for graph from data
    """
    # Create sorted set of nodes from to_nodes and from_nodes
    nodes = sorted(pd.unique(data[['from_node', 'to_node']].values.ravel()))

    # Create nodes from set
    for x in range(0, len(nodes)):
        globals()[nodes[x]] = Node(nodes[x])    # create node as global variable
        graph.add_node(globals()[nodes[x]])     # add node to graph

    # Add edge for row in csv -> from_node, to_node, weight
    for row in range(0, len(data)):
        to_node = globals()[data['to_node'][row]]
        from_node = globals()[data['from_node'][row]]
        graph.add_edge(from_node, to_node, data['weight_new'][row])
    
    return graph


def print_result(dist, prev):
    print("The quickest path from {} to {} is [{}] with a distance of {}".format(
        table_empty.label,
        pcstn.label,
        " -> ".join(to_array(prev, pcstn)),
        str(round(dist[pcstn], 2))
        )
    )


def main():
    graph = Graph()
    data = prepare_data(objects_at_once=1)
    data = calculate_distances(data)
    data = calculate_edge_weights(data)
    create_nodes_edges(graph, data)
    dist, prev = dijkstra(graph, table_empty)
    print_result(dist, prev)


main()
