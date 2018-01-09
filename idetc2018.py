import kaggle_analysis
import matplotlib.pyplot
import pkg_resources

# Define minimum values for an acceptable competition
minimum_true_teams = 10
minimum_solo_individuals = 10

# Find acceptable competitions
competition_info = kaggle_analysis.preprocessing.extract_good_teams(minimum_true_teams, minimum_solo_individuals)

# Compare nominal teams to true teams and individuals
kaggle_analysis.analysis.plot_team_size_histogram(competition_info)

# Compare nominal teams to true teams and individuals
real_team, indiv_team, nominal_team = kaggle_analysis.analysis.get_nominal_teams(competition_info)
kaggle_analysis.analysis.plot_nominal_teams(real_team, indiv_team, nominal_team)

# Plot performance v team size
matplotlib.pyplot.figure()
kaggle_analysis.analysis.plot_performance_v_size(real_team, indiv_team, "real_team.png")
kaggle_analysis.analysis.plot_nominal_performance_v_size(indiv_team, 24, 100, "nominal_team.png")
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Quality of Best Solution (Normalized)')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "performance_v_size.png"))

# TODO: Plot probability of winning for each team size
# TODO: Plot expected payout for each team size
# TODO: Plot expected payout per modicum of work
# TODO: Plot effort v team size for real teams
# TODO: Plot effort v performance for
