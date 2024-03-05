import os
import sys
try:
    from src.tsp import TSP
except ModuleNotFoundError:
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))
    from src.tsp import TSP

import pytest
import numpy as np


def test_tsp_get_solution_is_implemented():
    tsp = TSP(np.random.rand(3, 3))
    assert hasattr(tsp, "get_solution")
    assert callable(getattr(tsp, "get_solution"))


def test_tsp_get_solution_typing():
    # Test that the return type; Union[Tuple, List[int], np.ndarray]
    tsp = TSP(np.random.rand(3, 3))
    out = tsp.get_solution()
    assert isinstance(out, (tuple, list, np.ndarray))
