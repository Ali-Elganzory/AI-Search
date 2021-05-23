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


def update(event=None):
    global start_date, circle_radius, circle_colors, weight_text_shift, graph_updated

    # Drawing
    if is_graph_updated():
        # Clear the canvas
        ctx.clearRect(0, 0, window_width, window_height)
        ctx.save()

        # Style
        ctx.lineWidth = 4
        ctx.textAlign = "center"

        # Draw edges
        ctx.font = '20px serif'
        for node in search_agent.graph.values():
            selection_state = "unselected" if node.name is selected_node_name else "unselected"
            ctx.strokeStyle = circle_colors[selection_state]
            ctx.beginPath()
            for child_name, weight in node.children.items():
                ctx.moveTo(*node.position)
                ctx.lineTo(*search_agent.graph[child_name].position)

                dx = search_agent.graph[child_name].position[0] - \
                    node.position[0]
                dy = search_agent.graph[child_name].position[1] - \
                    node.position[1]
                if graph_type is directed:
                    # Cartesian calculations
                    distance = javascript.Math.sqrt(dx * dx + dy * dy)
                    new_x = search_agent.graph[child_name].position[0] - \
                        dx / distance * circle_radius
                    new_y = search_agent.graph[child_name].position[1] - \
                        dy / distance * circle_radius

                    # Transform to ease drawing the arrow head
                    ctx.translate(new_x, new_y)
                    ctx.rotate(javascript.Math.atan2(dy, dx))

                    # Draw arrow head
                    size = 8
                    ctx.moveTo(0, 0)
                    ctx.lineTo(-size, -size/2)
                    ctx.lineTo(-size, size/2)
                    ctx.lineTo(0, 0)
                    ctx.setTransform(1, 0, 0, 1, 0, 0)
                    ctx.fillText(weight, new_x + directed_weight_text_shift_in_x(dx, dy),
                                 new_y + directed_weight_text_shift_in_y(dx, dy))

                else:
                    ctx.fillText(weight, (node.position[0] +
                                          search_agent.graph[child_name].position[0]) / 2 + weight_text_shift_in_x(dx, dy),
                                 (node.position[1] + search_agent.graph[child_name].position[1]) / 2 + (-weight_text_shift))

            ctx.stroke()
            ctx.fill()

        # Draw nodes
        ctx.font = '16px serif'
        for node in search_agent.graph.values():
            selection_state = "selected" if node.name is selected_node_name else "unselected"
            ctx.strokeStyle = circle_colors[selection_state]
            ctx.beginPath()
            ctx.arc(*node.position,
                    circle_radius, 0, 2 * javascript.Math.PI)
            ctx.stroke()
            ctx.fillStyle = node_colors[node.state]
            ctx.fill()
            ctx.textBaseline = "middle"
            ctx.fillStyle = "black" if node_colors[node.state] is "white" else "white"
            ctx.fillText(node.name, node.position[0], node.position[1] - 8)
            ctx.fillText(f"h={node.heuristic}",
                         node.position[0], node.position[1] + 8)

        ctx.restore()
        graph_updated = False

    def request_again():
        window.requestAnimationFrame(update)

    window.setTimeout(request_again, 24)

    def advance_search_generator():
        next(search_generator)

    if search_agent.is_agent_searching:
        graph_updated = True
        try:
            now = javascript.Date.now()
            if now - start_date >= 800:
                window.setTimeout(advance_search_generator, 1)
                start_date = now
        except StopIteration as e:
            print("search_generator is empty")
        except Exception as e:
            pass


def weight_text_shift_in_x(dx, dy):
    global weight_text_shift
    return (weight_text_shift if dx < 0 else -weight_text_shift) if dy < 0 else (weight_text_shift if dx > 0 else -weight_text_shift)


def directed_weight_text_shift_in_x(dx, dy):
    global weight_text_shift
    return (2 * weight_text_shift if dx < 0 else 2 * -weight_text_shift)


def directed_weight_text_shift_in_y(dx, dy):
    global weight_text_shift
    return -(dy * 0.1 + weight_text_shift)


def mousemove(event):
    global selected_tool, search_agent, \
        node_counter, graph_updated, \
        selected_node_name, selected_edge_ends

    x = event.x
    y = event.y - 60

    def get_clicked_node_name(radius):
        for node in search_agent.graph.values():
            if x <= node.position[0] + radius and \
                    x >= node.position[0] - radius and \
                    y <= node.position[1] + radius and \
                    y >= node.position[1] - radius:
                return node.name
        return -1

    def get_clicked_edge_ends(radius):
        global weight_text_shift

        for node in search_agent.graph.values():
            for child_name in node.children:
                # Cartesian calculations
                dx = search_agent.graph[child_name].position[0] - \
                    node.position[0]
                dy = search_agent.graph[child_name].position[1] - \
                    node.position[1]

                if graph_type is directed:
                    distance = javascript.Math.sqrt(dx * dx + dy * dy)
                    textX = search_agent.graph[child_name].position[0] - \
                        dx / distance * circle_radius + \
                        directed_weight_text_shift_in_x(dx, dy)
                    textY = search_agent.graph[child_name].position[1] - \
                        dy / distance * circle_radius + \
                        directed_weight_text_shift_in_y(dx, dy)
                else:
                    textX = (node.position[0] +
                             search_agent.graph[child_name].position[0]) / 2 + weight_text_shift_in_x(dx, dy)
                    textY = (node.position[1] +
                             search_agent.graph[child_name].position[1]) / 2 + (-weight_text_shift)
                if x <= textX + radius and \
                        x >= textX - radius and \
                        y <= textY + radius and \
                        y >= textY - radius:
                    return (node.name, child_name)
        return -1

    # Modify the search_agent.graph with the appropriate tool
    if event.button == 0:
        node_name = get_clicked_node_name(circle_radius)
        if node_name == -1:
            if selected_tool is "add_node":
                if get_clicked_node_name(circle_radius * 3) == -1:
                    node_counter += 1
                    search_agent.graph[node_counter] = Node(
                        node_counter, (x, y), children={})
                    graph_updated = True
            elif selected_tool is "add_edge":
                selected_node_name = unselected
                graph_updated = True
            elif selected_tool is "delete_edge":
                selected_node_name = unselected
                graph_updated = True
            elif selected_tool is "update_weight":
                edge_ends = get_clicked_edge_ends(12)
                if edge_ends != -1:
                    selected_edge_ends = edge_ends
                    setInputDialogVisibility(True)
                    graph_updated = True
        else:
            if selected_tool is "toggle_goal":
                if search_agent.graph[node_name].state is "source":
                    return
                if search_agent.graph[node_name].state is "goal":
                    search_agent.graph[node_name].state = "empty"
                else:
                    search_agent.graph[node_name].state = "goal"
                    search_agent.graph[node_name].heuristic = 0
                graph_updated = True
            elif selected_tool is "update_heuristic":
                if search_agent.graph[node_name].state is not "goal":
                    selected_node_name = node_name
                    setInputDialogVisibility(True)
                graph_updated = True
            elif selected_tool is "delete_node":
                if search_agent.graph[node_name].state is not "source":
                    search_agent.graph.pop(node_name)
                    for node in search_agent.graph.values():
                        search_agent.graph[node.name].children.pop(
                            node_name, 99)
                    graph_updated = True
            elif selected_tool is "add_edge":
                if selected_node_name is unselected:
                    selected_node_name = node_name
                    graph_updated = True
                elif selected_node_name is not node_name:
                    if not child_exists(search_agent.graph[selected_node_name].children, node_name):
                        search_agent.graph[selected_node_name].children[node_name] = 99
                        if graph_type is undirected:
                            search_agent.graph[node_name].children[selected_node_name] = 99
                        selected_node_name = unselected
                        graph_updated = True
            elif selected_tool is "delete_edge":
                if selected_node_name is unselected:
                    selected_node_name = node_name
                    graph_updated = True
                elif selected_node_name is not node_name:
                    if child_exists(search_agent.graph[selected_node_name].children, node_name):
                        search_agent.graph[selected_node_name].children.pop(
                            node_name, 99)
                        if graph_type is undirected:
                            search_agent.graph[node_name].children.pop(
                                selected_node_name, 99)
                        selected_node_name = unselected
                        graph_updated = True


def child_exists(children, child_name):
    return child_name in children


def is_graph_updated():
    global graph_updated
    return graph_updated


# Setter for the [selected_tool]
def select_tool(tool):
    global selected_tool
    selected_tool = tool


# Setter for the [graph_type]
def select_graph_type(type):
    global graph_type, graph_updated

    graph_type = type
    search_agent.graph = {
        0: Node(0, (canvas.width / 2, canvas.height / 2), state="source", children={}),
    }
    graph_updated = True


# Weights dialog
def setInputDialogVisibility(state):
    global selected_node_name, selected_edge_ends, graph_updated
    if state:
        document["weights-modal"].showModal()
    else:
        document["weights-modal"].close()
        selected_node_name = unselected
        selected_edge_ends = unselected
        graph_updated = True


def updateHeuristic(node_name, heuristic):
    global graph_updated
    search_agent.graph[node_name].heuristic = heuristic
    graph_updated = True


def updateWeight(from_node, to_node, weight):
    global graph_updated
    search_agent.graph[from_node].children[to_node] = weight
    if graph_type is undirected:
        search_agent.graph[to_node].children[from_node] = weight
    graph_updated = True


def heuristicsDialogUpdate():
    validated = document["weights-form"].reportValidity()
    if validated:
        updateHeuristic(selected_node_name, int(
            document["weights-input"].value))
        setInputDialogVisibility(False)


def weightsDialogUpdate():
    validated = document["weights-form"].reportValidity()
    if validated:
        updateWeight(*selected_edge_ends, int(document["weights-input"].value))
        setInputDialogVisibility(False)


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
weight_text_shift = 10
circle_colors = {
    "unselected": "black",
    "selected": "red"
}
node_colors = {
    "empty": "white",
    "source": "red",
    "goal": "green",
    "visited": "purple",
    "path": "orange"
}
undirected = "undirected"
directed = "directed"


# Updates flags - Optimization measures
graph_updated = True


# Getting and setting canvas
canvas = document["canvas"]
ctx = canvas.getContext("2d")
window_width = window.innerWidth
window_height = window.innerHeight
canvas["width"] = window_width
canvas["height"] = window_height - (60 + 180 + 32 + 20)


# Search Agent
search_agent = SearchAgent({
    0: Node(0, (canvas.width / 2, canvas.height / 2), state="source", children={}),
})
graph_type = undirected
node_counter = 0


# Mapping tools to their respective colors
unselected = " "
selected_tool = "add_node"
selected_node_name = unselected
selected_edge_ends = unselected


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
document["toggle_goal"].bind("click", lambda e: select_tool("toggle_goal"))
document["update_heuristic"].bind(
    "click", lambda e: select_tool("update_heuristic"))
document["update_weight"].bind(
    "click", lambda e: select_tool("update_weight"))
document["canvas"].bind("mousedown", mousemove)


# Binding graph type buttons
document["undirected_graph"].bind("click",
                                  lambda e: select_graph_type(undirected))
document["directed_graph"].bind("click",
                                lambda e: select_graph_type(directed))


# Binding actions to weights modal
document["weights-close"].bind("click",
                               lambda e: setInputDialogVisibility(False))
document["weights-update"].bind("click", lambda e: heuristicsDialogUpdate(
) if selected_tool is "update_heuristic" else weightsDialogUpdate())


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
