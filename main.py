from browser import document, window

from Vector import Vector
from Particle import Particle


####	Functions	####

def window_updated():
	global width, height

	width = window.innerWidth
	height = window.innerHeight

	canvas["width"] = width
	canvas["height"] = height


def update(event=None):
	ctx.clearRect(0, 0, width, height)

	ctx.save()

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
	if (event.button == 0):
		grid[(event.y-top_padding)//cell_size][(event.x-left_padding)//cell_size] = selected_tool


def select_tool(tool):
	global selected_tool
	selected_tool = tool



####	Main		####

# Getting and setting canvas
canvas = document["canvas"]
ctx = canvas.getContext("2d")
width = window.innerWidth
height = window.innerHeight
canvas["width"] = width
canvas["height"] = height

# Constants
top_padding = 2 * 38 + 2 * 21
grid_dimensions = (10, 10)
grid = [["empty" for j in range(grid_dimensions[0])] for i in range(grid_dimensions[1])]
cell_size = 40
left_padding = (width - (grid_dimensions[0] * cell_size)) // 2

selected_tool = "blocked"
colors = { 
	"blocked": "gray",
	"empty": "white",
	"source": "red",
	"target": "green"
}

# Mouse event listeners
document["block"].bind("click", lambda e: select_tool("blocked"))
document["empty"].bind("click", lambda e: select_tool("empty"))
document["source"].bind("click", lambda e: select_tool("source"))
document["target"].bind("click", lambda e: select_tool("target"))
document["canvas"].bind("mousedown", mousemove)

# Eventloop
update()
