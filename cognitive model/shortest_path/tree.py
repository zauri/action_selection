class Node:
    def __init__(self, value=None, children=[], costs=[]):
        self.value = value
        self.children = children
        self.costs = costs


root = Node('root', [Node('a'), Node('b'), Node('c')], [1, 2, 3])
root.children[0].children = [Node('d'), Node('e')]
root.children[0].costs = [2, 3]
root.children[1].children = Node('f')
root.children[1].children = 2
