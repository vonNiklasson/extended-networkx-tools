from typing import Dict, Set, List, Tuple

import networkx
from random import randint


class Creator:
    """
    Static class that works with creating graph objects from given specifications.
    Can either create a random unassigned graph with given nodes or a graph with
    edges from given parameters.
    """

    @staticmethod
    def from_random(node_count: int) -> networkx.Graph:
        """
        Creates an unassigned graph with nodes of random position.
        The work area corresponds to the node count squared.

        :rtype: networkx.Graph
        :param node_count: The number of nodes to create a graph from.
        :return: An unassigned graph with nodes with random position.
        """
        area_dimension = node_count
        nxg: networkx.Graph = networkx.Graph()

        node_set: Set[str] = set()

        for node_id in range(0, node_count):
            coord_x = None
            coord_y = None
            # Keep finding new coordinates until a new one is found
            while coord_x is None or coord_y is None or str((coord_x, coord_y)) in node_set:
                coord_x = randint(0, area_dimension)
                coord_y = randint(0, area_dimension)
            nxg.add_node(node_id, x=coord_x, y=coord_y)
            node_set.add(str((coord_x, coord_y)))

        return nxg

    @staticmethod
    def from_spec(v: Dict[int, Tuple[int, int]], e: Dict[int, List[int]]) -> networkx.Graph:
        """
        Creates a graph from given parameters, that also assigns weighted edges based on a neighbour list.

        :param v: Nodes in the graph. Should be a dict with the format
                {  node_1: (x, y), node_2: (x, y)... }
        :param e: Edges that connects the nodes.Should be a dict with the format
                { node_1: [dest_1, dest_2, ...], node_2: [dest_3, dest_4, ...] }
        :return: A graph with assigned nodes and weighted edges.
        :rtype: networkx.Graph
        """
        nxg = networkx.Graph()

        for node_id, node in v.items():
            nxg.add_node(node_id, x=node[0], y=node[1])

        for origin, destinations in e.items():
            for destination in destinations:
                Creator.add_weighted_edge(nxg, origin, destination)

        return nxg

    @staticmethod
    def add_weighted_edge(nxg: networkx.Graph, origin: int, destination: int) -> bool:
        """
        Adds a bidirectional edge between 2 nodes with weight corresponding to the
        distance between the nodes squared.

        :param nxg: The graph to add an edge to.
        :param origin: First node id to add the edge from
        :param destination: Second node id to add the edge to.
        :return: True if the edge was added, otherwise false if the edge already existed.
        """
        if nxg.has_edge(origin, destination):
            return False

        # Find start and end coordinates
        start_coord = (nxg.node[origin]['x'], nxg.node[origin]['y'])
        destination_coord = (nxg.node[destination]['x'], nxg.node[destination]['y'])

        # Subtract the coordinate values of the two points
        delta = tuple(map(lambda n: pow(n[0] - n[1], 2), zip(start_coord, destination_coord)))
        # Extract values from delta tuple
        delta_x, delta_y = delta
        # Cost is the summation of the difference in x and y of the two coordinates
        weight = delta_x + delta_y

        # Add edge to graph with its corresponding weight
        nxg.add_edge(origin, destination, weight=weight)

        return True
