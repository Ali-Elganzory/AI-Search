import javascript

# test branch first commit
# Represents a state
class Node(object):
	"""docstring for Node"""
	def __init__(self, x, y, from_x, from_y, cost):
		self.x = x
		self.y = y
		self.from_x = from_x
		self.from_y = from_y
		self.cost = 1

	# Construct new node from a certain node [node]
	def from_node(self, node):
		return Node(self.x, self.y, node.x, node.y, node.cost + 1)


class SearchAgent(object):
	"""docstring for SearchAgent"""
	def __init__(self, dimensions):
		super(SearchAgent, self).__init__()
		self.__agent_status = "idle"
		self.__dimensions = dimensions
		self.grid = [["empty" for j in range(dimensions[0])] for i in range(dimensions[1])]

	@property
	def agent_status(self):
		return this.__agent_status

	@property
	def dimensions(self):
		return this.__dimensions

	# To reset the grid to its initial state
	def reset_grid(self):
		self.grid = list(map(lambda l: list(map(lambda c: c if c != "visited" else "empty", l)), self.grid))

	# Checks whether the state is the goal state (target)
	def is_goal_state(self, node):
		return self.grid[node.x][node.y] == "target"

	# Checks whether the new state is a valid state
	def is_valid_state(self, node):
		return not (node.x < 0 or node.x > self.__dimensions[0] \
			or node.y < 0 or node.y > self.__dimensions[1] or self.grid[i][j] != "empty")

	# Expand a node to its valid new states
	def expand(self, node):
		children = [Node(1, 0), Node(-1, 0), Node(0, 1), Node(0, -1)]
		return [new_node for new_node in map(lambda n: n.from_node(node), children) if is_valid_state(new_node)]

	@property
	def source(self):
		for i in range(self.__dimensions[0]):
			for j in range(self.__dimensions[1]):
				if self.grid[i][j] == "source":
					return Node(i, j, -1, -1)
		self.__agent_status = "no-source"
		return False

	def test(self):
		'''
		for i in range(self.__dimensions[0]):
			for j in range(self.__dimensions[1]):
				self.grid[i][j] = "visited"
				yield
		'''
		pass

	def breadth_first_search(node):
		self.reset_grid()
		fringe = []
		fringe.append(node)
		node == "visited"
		while fringe:
			node = fringe.pop[0]
			if is_goal_state (node):
				self.__agent_status = "success"
				return

			if node !="visited" :
				node == "visited"
				for i in expand (self,node):
					if node != "visited":
						fringe.append (i)
						i == "visited" # i guess there might be a mistake here
		 


	
	def depth_first_search(self):
		self.reset_grid()
		fringe = []
		fring.append(node)
		while fringe:
			node = fringe.pop() # pop(0) === queue and pop() === stack 
			if is_goal_state (node):
				self.__agent_status = "success"
				return
			if node != "visited" :
				node == "visited"
				for i in expand(self, node):
					if node != "visited":
						fringe.append(i)
	
	def depth_limit_search(self, limit):
		self.reset_grid()
		fringe = []
		fringe.append(node)
		while limit >= 0:
			node = fringe.pop()
			if is_goal_state (node):
				self.__agent_status = "success"
				return
			if node != "visited" :
				node == "visited"
				for i in expand(self, node):
					if node != "visited":
						fringe.append(i)
			limit = limit - 1
	
	def iterative_depth_search(self):
		self.reset_grid()
		fringe = []
		fringe.append(node)
		limit = -1
		iteration = 1
		while iteration < 100:
			limit = limit + 1
			while limit >= 0:
				node = fringe.pop()
				if is_goal_state (node):
					self.__agent_status = "success"
					return
				if node != "visited" :
					node == "visited"
					for i in expand(self, node):
						if node != "visited":
							fringe.append(i)
				limit = limit - 1
			iteration = iteration + 1
			
		if iteration = 100 :
			print("Error, the goal is not found!")
			return

		
	
	def uniform_cost_search(self):
		self.reset_grid()
		pass

	def greedy_search(self):
		self.reset_grid()
		pass

	def a_star_search(self):
		self.reset_grid()
		pass

