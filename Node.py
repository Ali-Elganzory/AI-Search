# Represents a [Node]
class Node(object):
    """docstring for Node"""

    def __init__(self, name, position, state="empty", cost=0, heuristic=1, children={}, path=[]):
        self.name = name
        self.state = state
        self.position = position
        self.heuristic = heuristic
        self.cost = cost
        self.children = children
        self.path = path

    def copy_from(node, cost, path):
        return Node(node.name, node.position, node.state, cost,
                    node.heuristic, node.children, path)
