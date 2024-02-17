import os
import warnings
from typing import List, Optional, Union, Tuple

import numpy as np
import tqdm


class TestResult:
    def __init__(self, name: str, percent_value: float, message: str = ""):
        self.name = name
        self.percent_value = percent_value
        self.message = message

    def __str__(self):
        _str = f'[{self.name}: {self.percent_value:.2f} %'
        if self.message:
            _str += f', ({self.message})'
        _str += ']'
        return _str


class TestCase:
    def run(self) -> TestResult:
        pass


class PerformanceTestCase(TestCase):
    @staticmethod
    def get_path_cost(adjacency_matrix: np.ndarray, path: Union[Tuple, List[int], np.ndarray]) -> float:
        adjacency_matrix = np.asarray(adjacency_matrix).squeeze()
        cost = 0
        for idx, i in enumerate(path[:-1]):
            weight = adjacency_matrix[i, path[idx + 1]]
            if np.isnan(weight):
                return np.inf
            cost += weight
        return cost

    @staticmethod
    def is_hamiltonian_cycle(adjacency_matrix: np.ndarray, path: Union[Tuple, List[int], np.ndarray]) -> bool:
        adjacency_matrix = np.asarray(adjacency_matrix).squeeze()
        if len(path) != adjacency_matrix.shape[0] + 1:
            return False
        if path[0] != path[-1]:
            return False
        unique_nodes = set(path[:-1])
        if len(unique_nodes) != adjacency_matrix.shape[0]:
            return False
        for idx, i in enumerate(path[:-1]):
            weight = adjacency_matrix[i, path[idx + 1]]
            if np.isnan(weight) or np.isinf(weight) or not np.isfinite(weight):
                return False
        return True

    def __init__(
            self,
            name: str,
            *,
            cls_to_test,
            constructor_inputs: List[Tuple] = None,
            get_solution_mth_name: str,
            expected_solutions: List,
    ):
        self.name = name
        self.cls_to_test = cls_to_test
        self.constructor_inputs = constructor_inputs if constructor_inputs is not None else []
        self.get_solution_mth_name = get_solution_mth_name
        self.expected_solutions = expected_solutions
        self._warnings = set()

    def compute_score(self, adjacency_matrix, solution, target_solution) -> float:
        if not self.is_hamiltonian_cycle(adjacency_matrix, solution):
            self._warnings.add("The solution is not a Hamiltonian cycle.")
            return 0.0
        obj_cost = self.get_path_cost(adjacency_matrix, solution)
        target_cost = self.get_path_cost(adjacency_matrix, target_solution)
        normalized_cost = target_cost / obj_cost
        score = np.nan_to_num(normalized_cost, nan=1.0, posinf=0.0, neginf=0.0)
        return score

    def run(self, verbose: bool = True):
        p_bar = tqdm.tqdm(self.constructor_inputs, desc=f"Running {self.name}", disable=not verbose)
        scores = []
        message = ""
        for i, constructor_input in enumerate(p_bar):
            target_solution = self.expected_solutions[i]
            try:
                cls_to_test = self.cls_to_test(*constructor_input)
            except Exception as e:
                return TestResult(self.name, 0.0, message=f"Error raised during instantiation: {e}")
            try:
                solution = getattr(cls_to_test, self.get_solution_mth_name)()
            except Exception as e:
                return TestResult(self.name, 0.0, message=f"Error raised during test: {e}")
            score = self.compute_score(constructor_input[0], solution, target_solution) * 100.0
            scores.append(score)
            p_bar.set_postfix(score=score)
        if self._warnings:
            warnings.warn(f"{self.name}: {' & '.join(self._warnings)}", RuntimeWarning)
            message = f"Warnings: {' & '.join(self._warnings)}"
        mean_score = np.mean(scores)
        result = TestResult(self.name, mean_score, message=message)
        p_bar.set_postfix_str(f"{result}")
        p_bar.close()
        return result


class PEP8TestCase(TestCase):
    MAX_LINE_LENGTH = 120

    def __init__(self, name: str, file_path: str):
        self.name = name
        self.file_path = file_path

    def run(self):
        import pycodestyle
        pep8style = pycodestyle.StyleGuide(ignore="W191,E501", max_line_length=self.MAX_LINE_LENGTH, quiet=True)
        result = pep8style.check_files([self.file_path])
        message = ', '.join(set([f"{key}:'{err_msg}'" for key, err_msg in result.messages.items()]))
        if result.counters['physical lines'] == 0:
            err_ratio = 0.0
        else:
            err_ratio = result.total_errors / result.counters['physical lines']
        percent_value = np.clip(100.0 - (err_ratio * 100.0), 0.0, 100.0).item()
        return TestResult(self.name, percent_value, message=message)


class CheckNotAllowedLibrariesTestCase(TestCase):
    def __init__(self, name: str, path: str, not_allowed_libraries: List[str], **kwargs):
        self.name = name
        self.path = path
        self.not_allowed_libraries = not_allowed_libraries
        self._warnings = set()
        self._excluded_files = kwargs.get("excluded_files", [])
        self._excluded_folders = kwargs.get("excluded_folders", [])

    def check_file(self, file_path: str) -> bool:
        with open(file_path, "r") as f:
            file_content = f.read()
        check = True
        for lib in self.not_allowed_libraries:
            if f"import {lib}" in file_content:
                self._warnings.add(f"The library '{lib}' is not allowed.")
                check = False
        return check

    def gather_files(self) -> List[str]:
        r"""
        Check if self.path is a file or a folder. If it is a file, return a list with only self.path. If it is a
        folder, return all the files in the folder and its subfolders.
        """
        if os.path.isfile(self.path):
            return [self.path]
        elif os.path.isdir(self.path):
            files = []
            for root, dirs, filenames in os.walk(self.path):
                if any([
                    os.path.normpath(excluded_folder) in os.path.normpath(root)
                    for excluded_folder in self._excluded_folders
                ]):
                    continue
                for filename in filenames:
                    if filename.endswith(".py") and filename not in self._excluded_files:
                        files.append(os.path.join(root, filename))
            return files
        else:
            raise ValueError(f"Invalid path: '{self.path}'.")

    def run(self):
        files = self.gather_files()
        score = 100.0
        message = ""
        for file_path in files:
            if not self.check_file(file_path):
                score = 0.0
        if self._warnings:
            warnings.warn(f"{self.name}: {' & '.join(self._warnings)}", RuntimeWarning)
            message = f"Warnings: {' & '.join(self._warnings)}"
        return TestResult(self.name, score, message=message)


class Tester:
    def __init__(self, tests: Optional[List[TestCase]] = None):
        if tests is None:
            tests = []
        self.tests = tests
        self.results = []

    def add_test(self, test: TestCase):
        self.tests.append(test)

    def run(self):
        for test in self.tests:
            test_result = test.run()
            self.results.append(test_result)
        return self.results

    def __str__(self):
        return "\n".join([str(result) for result in self.results])

    def to_file(self, file_path: str):
        with open(file_path, "w") as f:
            f.write(str(self))
        print(f"Test results saved to '{file_path}'.")
