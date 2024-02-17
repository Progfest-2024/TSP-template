from typing import Tuple, List, Union

import numpy as np


class TSP:
    def __init__(
            self,
            adjacency_matrix: np.ndarray,
    ):
        self.adjacency_matrix = adjacency_matrix # La matrice d'adjacence qui sera utilisée pour calculer le coût des chemins

    def get_solution(self) -> Union[Tuple, List[int], np.ndarray]:
        r"""
        Return a solution to the TSP problem.

        :Note: The list that is returned must be a cycle, i.e. the first and last elements must be the same.

        :return: A list of nodes representing a solution to the TSP problem.
        :rtype: Union[Tuple, List[int], np.ndarray]
        """
        path = np.random.permutation(self.adjacency_matrix.shape[0])
        cycle = np.concatenate((path, [path[0]]))
        return cycle
