from browser import document, window


####	Functions	####

def window_updated():
	global width, height

	width = window.innerWidth
	height = window.innerHeight

	canvas["width"] = width
	canvas["height"] = height


def update(event=None):
	# Clear the canvas
	ctx.clearRect(0, 0, width, height)
	ctx.save()

	# Draw the grid
	ctx.strokeStyle = "purple"
	ctx.beginPath()
	for i in range(grid_dimensions[0]):
		for j in range(grid_dimensions[1]):
			if grid[i][j] == "empty":
				ctx.strokeRect(left_padding + j*cell_size, i*cell_size, cell_size, cell_size)
			else:
				ctx.fillStyle = colors[grid[i][j]]
				ctx.fillRect(left_padding + j*cell_size, i*cell_size, cell_size, cell_size)
	
	ctx.restore()

	window.requestAnimationFrame(update)


def mousemove(event):
	# Return in case the event is out of the grid coordinates
	if event.x < left_padding or event.x > left_padding + (grid_dimensions[1] * cell_size) \
		or event.y < top_padding or event.y > top_padding + (grid_dimensions[0] * cell_size):
		return

	# Modify the grid with the appropriate tool
	if event.button == 0:
		grid[(event.y-top_padding)//cell_size][(event.x-left_padding)//cell_size] = selected_tool


# Setter for the [selected_tool]
def select_tool(tool):
	global selected_tool
	selected_tool = tool



####	Main		####

# Constants
grid_dimensions = (10, 10)
grid = [["empty" for j in range(grid_dimensions[0])] for i in range(grid_dimensions[1])]
cell_size = 40
top_padding = 1 * 38 + 2 * 24

# Getting and setting canvas
canvas = document["canvas"]
ctx = canvas.getContext("2d")
width = window.innerWidth
height = window.innerHeight
canvas["width"] = width
canvas["height"] = grid_dimensions[0] * cell_size

# Rest of constants that incorporate the canvas dimensions in calculation
left_padding = (width - (grid_dimensions[0] * cell_size)) // 2

# Mapping tools to their respective colors
selected_tool = "blocked"
colors = { 
	"blocked": "gray",
	"empty": "white",
	"source": "red",
	"target": "green"
}

# Binding listeners to tools and mousedown events
document["block"].bind("click", lambda e: select_tool("blocked"))
document["empty"].bind("click", lambda e: select_tool("empty"))
document["source"].bind("click", lambda e: select_tool("source"))
document["target"].bind("click", lambda e: select_tool("target"))
document["canvas"].bind("mousedown", mousemove)

# Eventloop
update()
