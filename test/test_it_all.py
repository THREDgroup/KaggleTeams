import unittest
import kaggle_analysis.preprocessing
import kaggle_analysis.analysis


class Test(unittest.TestCase):
    def test_it_all(self):
        minimum_true_teams = 10
        minimum_solo_individuals = 10
        competition_info = kaggle_analysis.preprocessing.extract_good_teams(minimum_true_teams,
                                                                            minimum_solo_individuals)
        real_team, indiv_team, nominal_team = kaggle_analysis.analysis.get_nominal_teams(competition_info)
        kaggle_analysis.analysis.plot_nominal_teams(real_team, indiv_team, nominal_team)
