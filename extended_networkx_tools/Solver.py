import networkx as nx

from Creator import Creator


class Solver:

    @staticmethod
    def path(nxg: nx.Graph):
        nodes = list(nxg.nodes())

        for edge in zip(nodes[:-1], nodes[1:]):
            x, y = edge
            Creator.add_weighted_edge(nxg, x, y)

        return nxg

    @staticmethod
    def cycle(nxg: nx.Graph):
        # Initially get the path of the graph
        nxg = Solver.path(nxg)

        # Get the start and destination node of the path
        nodes = nxg.nodes()
        start = min(nodes)
        destination = max(nodes)

        # Add the final edge for a cycle
        Creator.add_weighted_edge(nxg, start, destination)

        return nxg
