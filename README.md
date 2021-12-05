# AI-Search

Check this app at:
https://ali-elganzory.github.io/AI-Search/


# Description

An educational app for visualizing the different searching algorithms in the field of artificial intelligence by offering

- Undirected / Directed graph construction.
- Edge weights and state heuristics assignment.
- Multiple search algorithm choices.

## Supported Searching Algorithms

- Breadth First Search
- Depth First Search
- Depth Limit Search
- Iterative Deepening Search
- Uniform Cost Search
- Greedy Search
- A Star Search

# App Tech Stack

The app is built using HTML and Python as a website that can be run on any browser. To use the Web API, a Python-JavaScript transcompiler called Brython is used.

# Source Code

The app source code is attached with this document. Also, the app is source controlled by git and is available at this [repository](https://github.com/Ali-Elganzory/AI-Search). You can browse the incremental phases we followed to develop the app.

# How to Run

## Method 1

The app is deployed on GitHub Pages; Open this link [AI Search (ali-elganzory.github.io)](https://ali-elganzory.github.io/AI-Search/).

## Method 2

1 – Run the command [python -m http.server] in the root directory of the project to get an http server up and running – ready to serve the website.

2 – Open [http://localhost:8000/index.html](http://localhost:8000/index.html).

## Method 3

1 – Open the root directory of the project in Visual Studio Code.

2 – Install &quot;Live Server&quot; vscode extension.

3 – Click &quot;Go live&quot; at the right bottom of the editor; It will open the app website in your browser automatically.

# Use Instructions – Demo

1 – Open the app. The tools are labeled on the below figure.

![](/graphic/app_labeled.jpg)

</br>

2 – Start constructing the graph. You can

- Add a node by clicking where you want it to be drawn.
- Add an edge between two nodes A and B by clicking on A then B.
- Set / Remove a goal by clicking on any node – except the source.
- Set weights and heuristics by clicking on the edge weight text and nodes respectively.

An example graph is in the below figure.

![](/graphic/example_graph.jpg)

</br>
3 – Choose a searching algorithm from the bottom and click solve. The above graph is modified (goals, weights, and heuristics) and solved using A\* is shown below.
</br>
</br>

![](/graphic/searched_graph.jpg)

The agent starts to paint the visited nodes **purple** , and then, when it finds a goal, it paints the solution path with **orange** as seen in the above figure.
