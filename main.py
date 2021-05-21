from browser import document, window
import javascript

from SearchAgent import SearchAgent
from Node import Node

########################################
########		Functions		########
########################################


def window_updated():
    global window_width, window_height

    window_width = window.innerWidth
    window_height = window.innerHeight

    canvas["width"] = window_width
    canvas["height"] = window_height


# Dummy graph
graph = {
    0: Node(0, (340, 140), children=[(1, 20), (2, 13)]),
    1: Node(0, (420, 140), children=[(4, 45), (7, 67)]),
    2: Node(0, (420, 220), children=[(4, 90), (7, 18)]),
    4: Node(0, (340, 220), children=[]),
    7: Node(0, (360, 300), children=[]),
}


def update(event=None):
    global start_date, circle_radius, circle_colors

    # Drawing
    if updated():
        # Clear the canvas
        ctx.clearRect(0, 0, window_width, window_height)
        ctx.save()

        # Draw the grid
        ctx.lineWidth = 4
        ctx.strokeStyle = circle_colors["unselected"]
        for node in graph.values():
            ctx.beginPath()
            for edge in node.children:
                ctx.moveTo(*node.position)
                ctx.lineTo(*graph[edge[0]].position)
            ctx.stroke()

        for node in graph.values():
            ctx.beginPath()
            ctx.arc(*node.position,
                    circle_radius, 0, 2 * javascript.Math.PI)
            ctx.stroke()
            ctx.fillStyle = node_colors[node.state]
            ctx.fill()

        ctx.restore()

    def request_again():
        window.requestAnimationFrame(update)

    window.setTimeout(request_again, 24)

    def advance_search_generator():
        next(search_generator)

    if search_agent.is_agent_searching:
        try:
            now = javascript.Date.now()
            if now - start_date >= 500:
                window.setTimeout(advance_search_generator, 1)
                start_date = now
        except StopIteration as e:
            print("search_generator is empty")
        except Exception as e:
            pass


def mousemove(event):
	global selected_tool, graph, node_counter

	x = event.x
	y = event.y - 90

	def get_clicked_node_name():
		for node in graph.values():
			if x <= node.position[0] + circle_radius and \
					x >= node.position[0] - circle_radius and \
					y <= node.position[1] + circle_radius and \
					y >= node.position[1] - circle_radius:
				return node.name
		return -1

	# Modify the graph with the appropriate tool
	if event.button == 0:
		node_name = get_clicked_node_name()
		if node_name == -1:
			if selected_tool is "add_node":
				node_counter += 1
				graph[node_counter] = Node(node_counter, (x, y))
		else:
			graph.pop(node_name)


def updated():
    return True


# Setter for the [selected_tool]
def select_tool(tool):
    global selected_tool
    selected_tool = tool


# Setter for the [selected_search_algorithm]
def select_search_algorithm(search_algorithm):
    global selected_search_algorithm
    selected_search_algorithm = search_algorithm


def solve():
    global search_generator
    search_generator = alogorithms[selected_search_algorithm]()
    next(search_generator)


########################################
########		  Main		 	########
########################################
# Constants
circle_radius = 20
circle_colors = {
    "unselected": "black",
    "selected": "red"
}
node_colors = {
    "empty": "white",
    "source": "red",
    "target": "green",
    "visited": "purple",
    "path": "orange"
}

# Search Agent
search_agent = SearchAgent((20, 10))
node_counter = 100


# Getting and setting canvas
canvas = document["canvas"]
ctx = canvas.getContext("2d")
window_width = window.innerWidth
window_height = window.innerHeight
canvas["width"] = window_width
canvas["height"] = window_height - (90 + 220 + 40 + 20)


# Mapping tools to their respective colors
selected_tool = "add_node"


# Mapping actions to their respective search algorithms
selected_search_algorithm = "breadth-first"
alogorithms = {
    "breadth-first": search_agent.breadth_first_search,
    "depth-first": search_agent.depth_first_search,
    "depth-limit": lambda limit=3: search_agent.depth_limit_search(limit),
    "iterative-deepening": lambda max_limit=10: search_agent.iterative_deepening_search(max_limit),
    "uniform-cost": search_agent.uniform_cost_search,
    "greedy": search_agent.greedy_search,
    "a*": search_agent.a_star_search,
}


# Binding listeners to tools and mousedown events
document["add_node"].bind("click", lambda e: select_tool("add_node"))
document["add_edge"].bind("click", lambda e: select_tool("add_edge"))
document["delete_node"].bind("click", lambda e: select_tool("delete_node"))
document["delete_edge"].bind("click", lambda e: select_tool("delete_edge"))
document["canvas"].bind("mousedown", mousemove)


# Binding listeners to algorithms options and solve
document["breadth-first"].bind("click",
                               lambda e: select_search_algorithm("breadth-first"))
document["depth-first"].bind("click",
                             lambda e: select_search_algorithm("depth-first"))
document["uniform-cost"].bind("click",
                              lambda e: select_search_algorithm("uniform-cost"))
document["depth-limit"].bind("click",
                             lambda e: select_search_algorithm("depth-limit"))
document["iterative-deepening"].bind("click",
                                     lambda e: select_search_algorithm("iterative-deepening"))
document["greedy"].bind("click", lambda e: select_search_algorithm("greedy"))
document["a*"].bind("click", lambda e: select_search_algorithm("a*"))
document["solve"].bind("click", lambda e: solve())

# Eventloop
start_date = javascript.Date.now()
update()
