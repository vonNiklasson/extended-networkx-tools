from typing import List, Tuple, Union

from networkx import nx

try:
    from Creator import Creator
    from Analytics import Analytics
except ImportError:
    from .Creator import Creator
    from .Analytics import Analytics


class AnalyticsGraph:
    _graph: nx.Graph
    _old_graph = [List[Tuple[int, int, bool]]]

    _adjacency_matrix_sa: List[List[int]]
    _old_adjacency_matrix_sa: List[Tuple[int, int, int]]

    #_laplacian_matrix: List[List[int]]
    #_old_laplacian_matrix: List[Tuple[int, int, int]]

    _convergence_rate: float
    _old_convergence_rate: float
    _convergence_rate_dirty: bool
    _old_convergence_rate_dirty: bool

    _is_connected: bool
    _old_is_connected: bool
    _is_connected_dirty: bool
    _old_is_connected_dirty: bool

    _connectivity_nodes: Tuple[int, int]
    _old_connectivity_nodes: Union[Tuple[int, int], None]

    _edge_cost: int
    _old_edge_cost: int

    _dimension: int

    def __init__(self, nxg: nx.Graph):
        self._graph = nxg
        self._adjacency_matrix_sa = Analytics.get_adjacency_matrix(self._graph, True)
        #self._laplacian_matrix = Analytics.get_laplacian_matrix(self._graph)

        self._dimension = len(self._adjacency_matrix_sa)

        self._convergence_rate = None
        self._old_convergence_rate = None
        self._convergence_rate_dirty = True
        self._old_convergence_rate_dirty = True

        self._is_connected = None
        self._old_is_connected = None
        self._is_connected_dirty = True
        self._old_is_connected_dirty = True

        self._connectivity_nodes = None
        self._old_connectivity_nodes = None

        self._edge_cost = Analytics.total_edge_cost(self._graph)
        self._old_edge_cost = self._edge_cost

    def graph(self) -> nx.Graph:
        """
        Returns the graph instance that the class has been working on.

        :return: The current networkx graph instance.
        """
        return self._graph

    def get_convergence_rate(self) -> float:
        """
        Calculates the convergence rate for the current graph.

        :return:
        """
        if self._convergence_rate_dirty:
            # Convert the stochastic neighbour matrix to a stochastic one
            stochastic_neighbour_matrix = Analytics.get_stochastic_neighbour_matrix(
                adjacency_matrix=self._adjacency_matrix_sa
            )
            # Get the convergence rate
            self._convergence_rate = Analytics.convergence_rate(
                stochastic_neighbour_matrix=stochastic_neighbour_matrix
            )
            self._convergence_rate_dirty = False
        return self._convergence_rate

    def is_connected(self) -> bool:
        """
        Checks whether the graph is connected or not.

        :return:
        """
        if self._is_connected_dirty:
            if self._connectivity_nodes is None:
                self._is_connected = nx.is_connected(self._graph)
            else:
                self._is_connected = Analytics.is_nodes_connected_cuda(
                    mx=nx.to_numpy_matrix(self.graph(), weight=None),
                    origin=self._connectivity_nodes[0],
                    destination=self._connectivity_nodes[1]
                )
            self._is_connected_dirty = False
        return self._is_connected

    def get_edge_cost(self) -> float:
        """
        Calculates the edge cost for the current graph.

        :return:
        """
        return self._edge_cost

    def add_edge(self, origin, destination):
        if self.has_edge(origin, destination):
            return False
        self.reset_stage_actions()

        self._stage_graph(origin, destination, False)
        self._stage_is_connected()
        self._stage_convergence_rate()
        self._stage_edge_cost()

        Creator.add_weighted_edge(self._graph, origin, destination, ignore_validity=True)
        self._edge_cost += self._graph[origin][destination]['weight']
        self._set_adjacency_matrix_sa(origin, destination, 1)
        #self._laplacian_added_edge(origin, destination)

        self._convergence_rate_dirty = True
        # Is connected won't be dirty in this case

        return True

    def remove_edge(self, origin, destination):
        if not self.has_edge(origin, destination):
            return False
        self.reset_stage_actions()

        self._stage_graph(origin, destination, True)
        self._stage_is_connected()
        self._stage_convergence_rate()
        self._stage_edge_cost()

        self._edge_cost -= self._graph[origin][destination]['weight']

        self._graph.remove_edge(origin, destination)
        self._set_adjacency_matrix_sa(origin, destination, 0)
        #self._laplacian_removed_edge(origin, destination)

        self._convergence_rate_dirty = True
        self._is_connected_dirty = True
        self._connectivity_nodes = (origin, destination)

        return True

    def move_edge(self, origin, old_destination, new_destination):
        if old_destination == new_destination:
            return False
        if self.has_edge(origin, new_destination) or not self.has_edge(origin, old_destination):
            return False
        self.reset_stage_actions()

        self._stage_graph(origin, old_destination, True)
        self._stage_graph(origin, new_destination, False)
        self._stage_is_connected()
        self._stage_convergence_rate()
        self._stage_edge_cost()

        # Remove the old edge from the graph
        self._edge_cost -= self._graph[origin][old_destination]['weight']
        self._graph.remove_edge(origin, old_destination)
        self._set_adjacency_matrix_sa(origin, old_destination, 0)
        #self._laplacian_removed_edge(origin, old_destination)

        # Add the new edge to the graph
        Creator.add_weighted_edge(self._graph, origin, new_destination, ignore_validity=True)
        self._edge_cost += self._graph[origin][new_destination]['weight']
        self._set_adjacency_matrix_sa(origin, new_destination, 1)
        #self._laplacian_added_edge(origin, new_destination)

        self._convergence_rate_dirty = True
        self._is_connected_dirty = True
        self._connectivity_nodes = (origin, old_destination)

        return True

    def has_edge(self, origin, destination):
        """
        Checks whether the graph has an edge by looking up directly in a adjacency matrix.

        :param origin:
        :param destination:
        :return:
        """
        if origin == destination:
            return False
        return self._adjacency_matrix_sa[origin][destination] == 1

    def _set_adjacency_matrix_sa(self, origin, destination, val):
        """
        Sets a mirrored value for the _adjacency_matrix_sa matrix.

        :param origin:
        :param destination:
        :param val:
        """
        self._stage_adjacency_matrix_sa(origin, destination)

        self._adjacency_matrix_sa[origin][destination] = val
        self._adjacency_matrix_sa[destination][origin] = val

    def _laplacian_added_edge(self, origin, destination):
        """
        Updates the laplacian matrix based on adding an edge.

        :param origin:
        :param destination:
        """
        raise NotImplementedError
        self._stage_laplacian(origin, destination)

        self._laplacian_matrix[origin][destination] = -1
        self._laplacian_matrix[destination][origin] = -1

        self._laplacian_matrix[origin][origin] += 1
        self._laplacian_matrix[destination][destination] += 1

    def _laplacian_removed_edge(self, origin, destination):
        """
        Updates the laplacian matrix based on removing an edge.

        :param origin:
        :param destination:
        """
        raise NotImplementedError
        self._stage_laplacian(origin, destination)

        self._laplacian_matrix[origin][destination] = 0
        self._laplacian_matrix[destination][origin] = 0

        self._laplacian_matrix[origin][origin] -= 1
        self._laplacian_matrix[destination][destination] -= 1

    def _stage_laplacian(self, origin, destination):
        """
        Stages the values for the laplacian matrix.

        :param origin:
        :param destination:
        """
        self._old_laplacian_matrix += [
            (origin, destination, self._laplacian_matrix[origin][destination]),
            (destination, origin, self._laplacian_matrix[destination][origin]),
            (origin, origin, self._laplacian_matrix[origin][origin]),
            (destination, destination, self._laplacian_matrix[destination][destination]),
        ]

    def _stage_adjacency_matrix_sa(self, origin, destination):
        """
        Stages the values for the adjacency matrix with self-assignment.

        :param origin:
        :param destination:
        """
        self._old_adjacency_matrix_sa += [
            (origin, destination, self._adjacency_matrix_sa[origin][destination]),
            (destination, origin, self._adjacency_matrix_sa[destination][origin])
        ]

    def _stage_graph(self, origin, destination, edge):
        self._old_graph += [
            (origin, destination, edge)
        ]

    def _stage_convergence_rate(self):
        self._old_convergence_rate = self._convergence_rate
        self._old_convergence_rate_dirty = self._old_convergence_rate_dirty

    def _stage_is_connected(self):
        self._old_is_connected = self._is_connected
        self._old_is_connected_dirty = self._is_connected_dirty
        self._old_connectivity_nodes = self._connectivity_nodes

    def _stage_edge_cost(self):
        self._old_edge_cost = self._edge_cost

    def revert(self):
        # Revert the graph
        for action in self._old_graph:
            if action[2] is True:
                Creator.add_weighted_edge(self._graph, action[0], action[1], True)
            else:
                self._graph.remove_edge(action[0], action[1])

        # Revert the laplacian matrix
        #for action in self._old_laplacian_matrix:
        #    self._laplacian_matrix[action[0]][action[1]] = action[2]

        # Revert the adjacency matrix
        for action in self._old_adjacency_matrix_sa:
            self._adjacency_matrix_sa[action[0]][action[1]] = action[2]

        # Revert the convergence rate
        self._convergence_rate = self._old_convergence_rate
        self._convergence_rate_dirty = self._old_convergence_rate_dirty

        # Revert the is connected state
        self._is_connected = self._old_is_connected
        self._is_connected_dirty = self._old_is_connected_dirty
        self._connectivity_nodes = self._old_connectivity_nodes

        # Revert the edge cost
        self._edge_cost = self._old_edge_cost

    def reset_stage_actions(self):
        #self._old_laplacian_matrix = []
        self._old_adjacency_matrix_sa = []
        self._old_graph = []
        self._old_connectivity_nodes = None

    def get_adjacency_matrix_sa(self):
        return self._adjacency_matrix_sa

    def get_laplacian_matrix(self):
        raise NotImplementedError
        return self._laplacian_matrix

    def get_dimension(self):
        return self._dimension