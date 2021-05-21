# Represents a [Node]
class Node(object):
    """docstring for Node"""

    def __init__(self, name, position, cost=0, heuristic=1, children=[]):
        self.name = name
        self.state = "empty"
        self.position = position
        self.heuristic = heuristic
        self.cost = cost
        self.children = children

