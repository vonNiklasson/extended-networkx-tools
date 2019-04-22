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

### Visual

Is used to print a networkx graph to the screen, with its edges.

**Example output**:

![Example graph][examplegraph]

[examplegraph]: docs/source/_static/example-graph.png "Example graph"



## Usage

### Import


```python
from extended_networkx_tools import Creator, Analytics, Visual
```

