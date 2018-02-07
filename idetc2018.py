import kaggle_analysis
import numpy
import matplotlib.pyplot
import pkg_resources

# Define minimum values for an acceptable competition
minimum_true_teams = 10
minimum_solo_individuals = 10

# Find acceptable competitions
competition_info = kaggle_analysis.preprocessing.extract_good_teams(minimum_true_teams, minimum_solo_individuals)

# Calculate competition size
sizes = []
for competition in competition_info:
    sizes.append(len(competition["team_list"]))

competition_size = int(numpy.mean(sizes))
print(competition_size)

# Compare nominal teams to true teams and individuals
kaggle_analysis.analysis.plot_team_size_histogram(competition_info)

# Compare nominal teams to true teams and individuals
real_team, indiv_team, nominal_team = kaggle_analysis.analysis.get_nominal_teams(competition_info)
kaggle_analysis.analysis.plot_nominal_teams(real_team, indiv_team, nominal_team)

# # Plot performance v team size
matplotlib.pyplot.figure()
kaggle_analysis.analysis.plot_performance_v_size(real_team, indiv_team)
kaggle_analysis.analysis.plot_nominal_performance_v_size(indiv_team, 24, 100)
matplotlib.pyplot.xlim([2, 10])
matplotlib.pyplot.ylim([-1, 1.5])
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Quality of Best Solution (Normalized)')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "performance_v_size.png"))
#
# # Plot expected payout v team size
# matplotlib.pyplot.figure()
# kaggle_analysis.analysis.plot_payout_v_size(real_team, indiv_team, 10, 1000, competition_size)
# matplotlib.pyplot.xlim([1, 10])
# matplotlib.pyplot.xlabel('Team Size')
# matplotlib.pyplot.ylabel('Expected Payout (percentage of prize)')
# matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
# matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "payout_v_size.png"))
