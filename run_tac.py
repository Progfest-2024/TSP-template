import pickle
from importlib import import_module
from typing import Optional

import gdown
import tac
import os

from tac.perf_test_case import CheckNotAllowedLibrariesTestCase

from tools.tester import PerformanceTestCase


def get_data(data_file_path: str = "./data/data.pkl"):
    """
    This function downloads the data from Google Drive if it is not already present. You can run this function to
    download and inspect the data before running the tests.

    :param data_file_path: The path to the data file.
    :return: The data.
    :return: The data.
    """
    if os.path.exists(data_file_path):
        return pickle.load(open(data_file_path, "rb"))

    url = 'https://drive.google.com/uc?id=1R8TF0BdUbKF-Z6yiDPNFIFo91ewvPxF2'
    os.makedirs(os.path.dirname(data_file_path), exist_ok=True)
    gdown.download(url, data_file_path, quiet=False)
    return pickle.load(open(data_file_path, "rb"))


def run_tac(
        repo_url: Optional[str] = None,
        path_to_root=".",
        weights=None,
):
    code_source = tac.SourceCode(os.path.join(path_to_root, "src"), url=repo_url, logging_func=print)
    default_weights = {
        tac.Tester.PEP8_KEY: 10.0,
        tac.Tester.CODE_COVERAGE_KEY: 0.0,
    }
    if weights is None:
        weights = {}
    weights = {**default_weights, **weights}

    auto_corrector = tac.Tester(
        code_source,
        tests_src=tac.TesterInput.NULL,
        report_dir="tmp_report_dir",
        logging_func=print,
        weights=weights,
    )
    auto_corrector.setup_at()
    lib_tester = CheckNotAllowedLibrariesTestCase(
        name="Check not allowed libraries",
        path=code_source.local_path,
        not_allowed_libraries=["networkx"],
        excluded_folders=[
            os.path.join(code_source.working_dir, "venv"),
            os.path.join(code_source.working_dir, "__pycache__")
        ],
    )
    auto_corrector.add_test(lib_tester)

    data_file_path = os.path.join(os.path.dirname(__file__), "data/data.pkl")
    data = get_data(data_file_path=data_file_path)

    filename = f".tsp"
    file_root_importlike = os.path.normpath(code_source.local_path).replace(
        './', '').replace('/', '.').replace('\\', '.')
    cls_to_test = getattr(import_module(filename, file_root_importlike), "TSP")

    performance_test = PerformanceTestCase(
        name=f"Performance Test on {len(data)} graphs",
        weigth=10.0,
        cls_to_test=cls_to_test,
        constructor_inputs=[(datum["adjacency_matrix"],) for datum in data],
        get_solution_mth_name="get_solution",
        expected_solutions=[datum["best_path"] for datum in data],
    )
    auto_corrector.add_test(performance_test)

    auto_corrector.run(
        overwrite=False,
        debug=True,
        clear_temporary_files=False,
        clear_pytest_temporary_files=False,
    )
    auto_corrector.rm_report_dir()
    auto_corrector.report.save()
    print(auto_corrector.report)
    return auto_corrector.report


if __name__ == "__main__":
    run_tac()
