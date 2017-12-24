import kaggle_analysis


# Define minimum values for an acceptable competition
minimum_true_teams = 10
minimum_solo_individuals = 10

# Find acceptable competitions
competition_info = kaggle_analysis.preprocessing.extract_good_teams(minimum_true_teams, minimum_solo_individuals)

# Compare nominal teams to true teams and individuals
kaggle_analysis.analysis.plot_team_size_histogram(competition_info)

# Compare nominal teams to true teams and individuals
kaggle_analysis.analysis.nominal_teams(competition_info)

# TODO: Add analysis of performance as function of true team size
# TODO: Add analysis fo performance as function of nominal team size
# TODO: Probability of winning for each nominal team size divided by team size
# TODO: Probability of winning for each true team size divided by team size