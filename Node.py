# Represents a [Node]
class Node(object):
    """docstring for Node"""

    def __init__(self, name, position, state="empty", cost=0, prev_cost = 0, heuristic=1, children={}, path=[], fringed = 0):
        self.name = name
        self.state = state
        self.position = position
        self.heuristic = heuristic
        self.cost = cost
        self.children = children
        self.path = path
        self.fringed = fringed
        self.prev_cost = prev_cost

    def copy_from(node, cost, path):
        return Node(node.name, node.position, node.state, cost, node.cost,
                    node.heuristic, node.children, path, node.fringed)
