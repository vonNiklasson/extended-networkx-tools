import networkx
try:
    from Creator import Creator
except ImportError:
    from .Creator import Creator


class Solver:
    """
    Class to add edges to given networkx grahps taken from simple Graph Theory, such as path and cycle.
    """

    @staticmethod
    def path(nxg: networkx.Graph) -> networkx.Graph:
        """
        Adds edges to a given graph as a path, such as the following:
        (0, 1), (1, 2), ... (n-1, n)

        :rtype: networkx.Graph
        :param nxg: A graph with nodes containing coordinates.
        :return: A graph with connected nodes such as they form a path.
        """
        nodes = list(nxg.nodes())

        for edge in zip(nodes[:-1], nodes[1:]):
            x, y = edge
            Creator.add_weighted_edge(nxg, x, y)

        return nxg

    @staticmethod
    def cycle(nxg: networkx.Graph) -> networkx.Graph:
        """
        Adds edges to a given graph as a path, such as the following:
        (0, 1), (1, 2), ... (n-1, n), (n, 0)

        :rtype: networkx.Graph
        :param nxg: A graph with nodes containing coordinates.
        :return: A graph with connected nodes such as they form a cycle.
        """
        # Initially get the path of the graph
        nxg = Solver.path(nxg)

        # Get the start and destination node of the path
        nodes = nxg.nodes()
        start = min(nodes)
        destination = max(nodes)

        # Add the final edge for a cycle
        Creator.add_weighted_edge(nxg, start, destination)

        return nxg
