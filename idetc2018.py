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
nt, pt, et = kaggle_analysis.analysis.analyze_team_performance_v_size(real_team, indiv_team, std=False)
nn, pn, en = kaggle_analysis.analysis.analyze_nominal_team_performance_v_size(indiv_team, 24, 1000, std=False)

matplotlib.pyplot.figure()
matplotlib.pyplot.errorbar(nt[1:8], pt[0][1:8], pt[1][1:8])
matplotlib.pyplot.errorbar(nn[1:8], pn[0][1:8], pn[1][1:8])
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Quality of Best Solution (Normalized)')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "performance_v_size.png"))

matplotlib.pyplot.figure()
matplotlib.pyplot.errorbar(nt[1:8], et[0][1:8], et[1][1:8])
matplotlib.pyplot.errorbar(nn[1:8], en[0][1:8], en[1][1:8])
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Total Submissions (Normalized)')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "effort_v_size.png"))

# Plot expected payout v team size
matplotlib.pyplot.figure()
team_sizes = range(2, 9, 1)
team_pay, team_win, nominal_pay, nominal_win = kaggle_analysis.analysis.analyze_payout_v_size(real_team, indiv_team, team_sizes, 10000, competition_size)
matplotlib.pyplot.errorbar(team_sizes, team_win[0], team_win[1])
matplotlib.pyplot.errorbar(team_sizes, nominal_win[0], nominal_win[1])
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Probability of Winning')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "win_perct_v_size.png"))

matplotlib.pyplot.figure()
matplotlib.pyplot.errorbar(team_sizes, team_pay[0], team_pay[1])
matplotlib.pyplot.errorbar(team_sizes, nominal_pay[0], nominal_pay[1])
matplotlib.pyplot.xlabel('Team Size')
matplotlib.pyplot.ylabel('Expected Payout Per Person')
matplotlib.pyplot.legend(['True Teams', 'Nominal Teams'])
matplotlib.pyplot.savefig(pkg_resources.resource_filename("figures", "payout_v_size.png"))

