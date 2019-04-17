from typing import Dict, Any, Set, List, Tuple

import networkx as nx
from random import randint


class Creator:

    def __init__(self):
        pass

    @classmethod
    def from_random(cls, node_count):
        area_dimension = node_count
        nxg: nx.Graph = nx.Graph()

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

    @classmethod
    def from_spec(cls, v: Dict[int, Tuple[int, int]], e: Dict[int, List[int]]):
        """

        :param v:
        :param e:
        :return:
        :rtype: networkx.Graph
        """
        nxg = nx.Graph()  # type: nx.Graph

        for node_id, node in v.items():
            nxg.add_node(node_id, x=node[0], y=node[1])

        for origin, destinations in e.items():
            for destination in destinations:
                Creator.add_edge(nxg, origin, destination)

        return nxg

    @staticmethod
    def add_edge(g, start, destination):

        if g.has_edge(start, destination):
            return False

        # Find start and end coordinates
        start_coord = (g.node[start]['x'], g.node[start]['y'])
        destination_coord = (g.node[destination]['x'], g.node[destination]['y'])

        # Subtract the coordinate values of the two points
        delta = tuple(map(lambda n: pow(n[0] - n[1], 2), zip(start_coord, destination_coord)))
        # Extract values from delta tuple
        deltax, deltay = delta
        # Cost is the summation of the difference in x and y of the two coordinates
        weight = deltax + deltay

        # Add edge to graph with its corresponding weight
        g.add_edge(start, destination, weight=weight)

        return True
