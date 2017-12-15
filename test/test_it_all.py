import unittest
import kaggle_analysis.preprocessing
import kaggle_analysis.analysis


class Test(unittest.TestCase):
    def test_it_all(self):
        kaggle_analysis.analysis.nominal_teams(kaggle_analysis.preprocessing.extract_good_teams(10, 10))
