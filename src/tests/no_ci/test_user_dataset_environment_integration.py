## Test dataset information
import unittest

from src.data import Dataset


class TestDatasets(unittest.TestCase):
    """
    Basic smoke tests to ensure that all of the available datasets
    load and have some expected property.
    """
    def basic_unit_test(self):
        assert True

    def test_penguins_clean(self):
        ds = Dataset.load('penguins-clean')

    def test_penguins_challenge(self):
        ds = Dataset.load('penguins-clean')
        ### There is a typo in this test and it will fail.
        ### Please fix it!
        assert ds.data.shape == (334, 4)

    def test_penguins_scaled(self):
        ds = Dataset.load('penguins-scaled')
        assert len(ds.data) == 334
