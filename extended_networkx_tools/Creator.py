from typing import Dict, Set, List, Tuple

import networkx as nx
from random import randint


class Creator:

    @staticmethod
    def from_random(node_count):
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

    @staticmethod
    def from_spec(v: Dict[int, Tuple[int, int]], e: Dict[int, List[int]]):
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
                Creator.add_weighted_edge(nxg, origin, destination)

        return nxg

    @staticmethod
    def add_weighted_edge(nxg, start, destination):

        if nxg.has_edge(start, destination):
            return False

        # Find start and end coordinates
        start_coord = (nxg.node[start]['x'], nxg.node[start]['y'])
        destination_coord = (nxg.node[destination]['x'], nxg.node[destination]['y'])

        # Subtract the coordinate values of the two points
        delta = tuple(map(lambda n: pow(n[0] - n[1], 2), zip(start_coord, destination_coord)))
        # Extract values from delta tuple
        delta_x, delta_y = delta
        # Cost is the summation of the difference in x and y of the two coordinates
        weight = delta_x + delta_y

        # Add edge to graph with its corresponding weight
        nxg.add_edge(start, destination, weight=weight)

        return True
