## Test dataset information
import logging
import unittest

from src.data import Dataset
from src import workflow
from src.log import logger
from src.utils import run_notebook
from src import paths


class TestDatasetsSmall(unittest.TestCase):
    """
    Basic smoke tests to ensure that the smaller (and more quickly processed)
    available datasets load and have some expected property.
    """
    def test_penguins_raw(self):
        ds = Dataset.load('penguins-raw')

    # should likely comment this out for the tutorial itself
    def test_notebook_04(self):
        run_notebook(notebook_name="04-Data-Challenge.ipynb",
             notebook_path=paths['notebook_path'],
             output_notebook_name="04-Data-Challenge-Test-Run.ipynb",
             output_notebook_path=paths['notebook_path'])
        ds = Dataset.load('penguins-clean')
        ds = Dataset.load('penguins-scaled')

    def test_notebook_03(self):
        run_notebook(notebook_name="03-Repo-Challenge.ipynb",
             notebook_path=paths['notebook_path'],
             output_notebook_name="03-Repo-Challenge-Test-Run.ipynb",
             output_notebook_path=paths['notebook_path'])

    def test_notebook_02(self):
        run_notebook(notebook_name="02-Environment-Challenge.ipynb",
             notebook_path=paths['notebook_path'],
             output_notebook_name="02-Environment-Challenge-Test-Run.ipynb",
             output_notebook_path=paths['notebook_path'])

def test_logging_is_debug_level():
    assert logger.getEffectiveLevel() == logging.DEBUG
