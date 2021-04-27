import javascript


# Represents a state
class Node(object):
	"""docstring for Node"""
	def __init__(self, x, y, from_x=-1, from_y=-1, cost=1):
		self.x = x
		self.y = y
		self.from_x = from_x
		self.from_y = from_y
		self.cost = cost

	# Construct new node from a certain node [node]
	def from_node(self, node):
		return Node(self.x + node.x, self.y + node.y, node.x, node.y, node.cost + 1)


class SearchAgent(object):
	"""docstring for SearchAgent"""
	def __init__(self, dimensions):
		super(SearchAgent, self).__init__()
		self.__agent_status = "idle"
		self.__dimensions = dimensions
		self.grid = [["empty" for j in range(dimensions[0])] for i in range(dimensions[1])]

	################################################
	########		Utility Functions		########
	################################################

	@property
	def dimensions(self):
		return this.__dimensions

	@property
	def agent_status(self):
		return this.__agent_status

	@property
	def is_agent_searching(self):
		return self.__agent_status == "searching"

	# Reserve the agent and prevent starting new alogorithms while searching
	def reserve_agent(self):
		if self.__agent_status == "searching":
			return False
		self.__agent_status = "searching"
		return True

	# To reset the grid to its initial state
	def reset_grid(self):
		self.grid = list(map(lambda l: list(map(lambda c: c if c in ["blocked", "source", "target"] else "empty", l)), self.grid))

	# The state of a certain node
	def node_state(self, node):
		return self.grid[node.x][node.y]

	# Checks whether the state is the goal state (target)
	def is_goal_state(self, node):
		return self.node_state(node) == "target"

	# Checks whether the new state is a valid state
	def is_valid_state(self, node):
		return not (node.x < 0 or node.x >= self.__dimensions[0] \
			or node.y < 0 or node.y >= self.__dimensions[1]) and self.node_state(node) in ["empty", "target"]

	# Expand a node to its valid new states
	def expand(self, node):
		children = [Node(1, 0), Node(-1, 0), Node(0, 1), Node(0, -1)]
		return list(filter(self.is_valid_state, map(lambda n: n.from_node(node), children)))

	# Get the source node (start state)
	@property
	def source(self):
		for i in range(self.__dimensions[0]):
			for j in range(self.__dimensions[1]):
				if self.grid[i][j] == "source":
					return Node(i, j, -1, -1)
		self.__agent_status = "no-source"
		return False

	# Finished with "success" or "failed"
	def finished(self, result, source):
		self.__agent_status = result
		self.grid[source.x][source.y] = "source"

	def test(self):
		pass


	################################################
	########		Search Algorithms		########
	################################################

	def breadth_first_search(self):
		source = self.source
		if not (source != False and self.reserve_agent()):
			return

		self.reset_grid()
		fringe = []
		node = source
		fringe.append(node)

		while fringe:
			node = fringe.pop(0)
			if self.is_goal_state(node):
				self.finished("success", source)
				return

			if self.node_state(node) != "visited":
				self.grid[node.x][node.y] = "visited"
				for n in self.expand(node):
					if self.node_state(n) != "visited":
						fringe.append(n)
				yield

		self.finished("failed", source)

	
	def depth_first_search(self):
		self.reset_grid()
		pass
	
	def uniform_cost_search(self):
		self.reset_grid()
		pass

	def greedy_search(self):
		self.reset_grid()
		pass

	def a_star_search(self):
		self.reset_grid()
		pass

