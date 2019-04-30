# Extended networkx Tools
Python Package for for visualizing and converting networkx graphs.

## Introduction

This package was created for the purpose of examining bidirectional graphs with respect to its convergence rate and edge costs.

## Installation

```shell
pip install extended-networkx-tools
```

## Documentation

[extended-networkx-tools.readthedocs.io](https://extended-networkx-tools.readthedocs.io/)

## The package

Currently the package contains 3 main modules, `Creator`, `Analytics` and `Visual`.

### Creator

Contains tools to create networkx graphs based on given parameters, such as randomly 
create an empty graph based on a number of nodes, or specify precisely the 
coordinates of nodes and the edges between them.

### Analytics

Has tools for analysing the networkx object and extract useful information from it, such 
as convergence rate, neighbour matrix, its eigenvalues.

### Solver

Used to find simple greedy solutions to a connected graph taken from graph theory. The current approaches are:

- ``path``: Adds edges as a path from the start to end node
- ``cycle``: Adds edges just like the path, but also one edge from the start to end node.
- ``complete``: Adds edges between all nodes to all the other nodes, such as the maximum distance between every node is one.

### Visual

Is used to print a networkx graph to the screen, with its edges.

[Example output graph][examplegraph]

[examplegraph]: docs/source/_static/example-graph.png "Example graph"

### AnalyticsGraph

The `AnalyticsGraph` class is a helper class that serves the purpose of a wrapper object
that can do all calculations based on changes done to the graph, rather
than recalculating every metric after simple changes. Such as the connectivity state
will stay the same after adding an edge.

There is also options to revert changes and keep previous calculations.

**Example usage**:

```python
from extended_networkx_tools import Creator, Solver, AnalyticsGraph

# Create a random graph with a path
g = Creator.from_random(10)
g = Solver.path(g)

# Convert the graph to an AnalytcsGraph object
ag = AnalyticsGraph(g)

convergence_rate = ag.get_convergence_rate() # Calcualtes the convergence rate from scratch
ag.remove_edge(4, 5)    # Removes an edge
ag.revert()             # Revert the changes
convergence_rate = ag.get_convergence_rate() # Doesn't calculate it since it's saved from previous state
```

## Usage

### Import


```python
from extended_networkx_tools import Creator, Analytics, Visual, Solver, AnalyticsGraph
```

