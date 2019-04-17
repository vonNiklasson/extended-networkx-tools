from typing import List

import numpy as np
from numpy import linalg as LA


class Tools:

    @staticmethod
    def get_neighbour_matrix(g) -> List[List[float]]:
        """
        Creates a adjacency matrix for a specified graph: g, each row represents a node in the graph
        where the values in each column represents if there is an edge or not between those nodes.

        :param g: Networkx bi-directional graph object
        :return A: List of rows, representing the adjacency matrix.
        """
        # Sort the nodes in the graph
        s_nodes = list(g.nodes())
        s_nodes.sort()
        # Get the dimension of each row
        dim = len(s_nodes)

        mx = []
        for node in g.nodes():
            row = [0] * dim
            # Get the index of the current node
            node_index = s_nodes.index(node)
            row[node_index] = 1
            for neighbour in g.neighbors(node):
                node_index = s_nodes.index(neighbour)
                row[node_index] = 1
            mx.append(row)
        return mx

    @staticmethod
    def get_stochastic_neighbour_matrix(g):
        """
        Creates a stochastic adjacency matrix for a specified graph: g, each row represents a node in the graph
        where the values in each column represents if there is an edge or not between those nodes.
        The values for each neighbour is represented by 1/(number of neighbours), if no edge exists this value is 0.

        :param g: Networkx bi-directional graph object
        :return A: List of rows, representing the adjacency matrix
        """
        # Get the neighbour matrix
        mx = Tools.get_neighbour_matrix(g)

        # Iterate over each row
        for row_id, _ in enumerate(mx):
            # Calculate the sum for each row
            row_sum = sum(mx[row_id])
            # Divide each node in the row with the sum of the row
            mx[row_id] = list(map(lambda x: (x / row_sum), mx[row_id]))

        # Working solution that might however be worse than the previous solution.
        # mx = list(map(lambda row: list(map(lambda cell: cell / sum(row), row)), mx))

        return mx



    @staticmethod
    def get_eigenvalues(a):
        """
        Simple function to retrieve the eigenvalues of matrix a
        :param a: list containing lists of rows representing a matrix
        :return w: list of eigen values
        """
        
        A = np.array(a)
        w, _ = LA.eig(A)
        return w

    @staticmethod
    def second_largest(numbers: List[float]) -> float:
        """
        Simple function to return the 2nd largest number in a list of numbers.

        :param numbers: A list of numbers
        :return float: The 2nd largest number in the list numbers
        :rtype: float

        """
        count = 0
        m1 = m2 = float('-inf')
        for x in numbers:
            count += 1
            if x > m2:
                if x >= m1:
                    m1, m2 = x, m1
                else:
                    m2 = x
        return m2 if count >= 2 else None

    @staticmethod
    def convergence_rate(g) -> float:
        """
        Function to retrieve the 2nd largest eigenvalue in the adjacency matrix of a graph

        :param g: Networkx bi-directional graph object
        :return: The 2nd largest eigenvalue of the adjacency matrix
        :rtype: float
        """
        A = Tools.get_stochastic_neighbour_matrix(g)
        ev = Tools.get_eigenvalues(A)
        return Tools.second_largest(ev)

    @staticmethod
    def total_edge_cost(g) -> float:
        """
        Calculates the total cost of all edges in the given graph

        :param g: A networkx object with nodes and edges.
        :type g: networkx.Graph
        :return: The total cost of all edges in the graph.
        :rtype: float
        """
        total = 0
        edges = g.edges(data=True)

        for edge in edges:
            total += edge['weight']
            
        return total
