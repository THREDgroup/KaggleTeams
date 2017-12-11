import numpy
import matplotlib.pyplot
import utils

p = 0.05
good_competitions = numpy.load("good_competitions.npz")["good_competitions"]

real_team_scores_all = []
indiv_team_scores_all = []
remixed_team_scores_all = []
real_team_mefforts_all = []
indiv_team_mefforts_all = []
remixed_team_mefforts_all = []
real_team_tefforts_all = []
indiv_team_tefforts_all = []
remixed_team_tefforts_all = []

for competition in good_competitions:
    real_team_scores = []
    indiv_team_scores = []
    real_team_mefforts = []
    indiv_team_mefforts = []
    real_team_tefforts = []
    indiv_team_tefforts = []


    # Check directionality
    diffscore = competition["team_list"][0]["Score"] - competition["team_list"][1]["Score"]
    diffrank = competition["team_list"][0]["Ranking"] - competition["team_list"][1]["Ranking"]
    if diffscore*diffrank < 0:
        m = -1
    else:
        m = 1

    # Assess quality of teams and individuals
    for team in competition["team_list"]:

        effort = 0
        for userkey in team["user_list"]:
            effort += team["user_list"][userkey]

        if len(team["user_list"]) == 1:
            indiv_team_scores.append(m*team["Score"])
            indiv_team_mefforts.append(effort)
            indiv_team_tefforts.append(effort)
        else:
            real_team_scores.append(m*team["Score"])
            real_team_mefforts.append(effort/len(team["user_list"]))
            real_team_tefforts.append(effort)

    # Normalize values according to mean and standard distribution
    mm = numpy.mean(indiv_team_scores)
    sm = numpy.std(indiv_team_scores)
    real_team_scores = [(x-mm)/sm for x in real_team_scores]
    indiv_team_scores = [(x-mm)/sm for x in indiv_team_scores]

    # Normalize values according to mean and standard distribution
    mm = numpy.mean(indiv_team_mefforts)
    real_team_mefforts = [x/mm for x in real_team_mefforts]
    indiv_team_mefforts = [x/mm for x in indiv_team_mefforts]

    # Normalize values according to mean and standard distribution
    mm = numpy.mean(indiv_team_tefforts)
    real_team_tefforts = [x/mm for x in real_team_tefforts]
    indiv_team_tefforts = [x/mm for x in indiv_team_tefforts]

    # Get scores for teams resampled from individuals
    remixed_team_scores = []
    remixed_team_mefforts = []
    remixed_team_tefforts = []
    for _ in range(int(0.5*len(competition["team_list"]))):
        # Choose a team size
        team_size = numpy.random.choice(competition["real_team_sizes"])

        # Get remixed average effort
        efforts = numpy.random.choice(indiv_team_mefforts, team_size, replace=False)
        remixed_team_mefforts.append(numpy.mean(efforts))
        remixed_team_tefforts.append(numpy.sum(efforts))

        # Get remixed scores
        scores = numpy.random.choice(indiv_team_scores, team_size, replace=False)
        remixed_team_scores.append(numpy.min(scores))


    # Save sores
    real_team_scores_all += real_team_scores
    indiv_team_scores_all += indiv_team_scores
    remixed_team_scores_all += remixed_team_scores

    real_team_mefforts_all += real_team_mefforts
    indiv_team_mefforts_all += indiv_team_mefforts
    remixed_team_mefforts_all += remixed_team_mefforts

    real_team_tefforts_all += real_team_tefforts
    indiv_team_tefforts_all += indiv_team_tefforts
    remixed_team_tefforts_all += remixed_team_tefforts

total = len(good_competitions)

matplotlib.pyplot.figure()

matplotlib.pyplot.plot(numpy.mean(indiv_team_tefforts_all), -numpy.mean(indiv_team_scores_all), 'rs')
matplotlib.pyplot.plot(numpy.mean(real_team_tefforts_all), -numpy.mean(real_team_scores_all), 'bo')
matplotlib.pyplot.plot(numpy.mean(remixed_team_tefforts_all), -numpy.mean(remixed_team_scores_all), 'g^')

delta = 0.1
utils.plot_slope(numpy.array([0.9, 1.1]), indiv_team_tefforts_all, indiv_team_scores_all, 'r-')
utils.plot_slope(numpy.mean(real_team_tefforts_all)+[-delta, delta], real_team_tefforts_all, real_team_scores_all, 'b-')
utils.plot_slope(numpy.mean(remixed_team_tefforts_all)+[-delta, delta], remixed_team_tefforts_all, remixed_team_scores_all, 'g-')
utils.plot_slope(numpy.array([1.0, numpy.mean(remixed_team_tefforts_all)]), indiv_team_tefforts_all, indiv_team_scores_all, 'r:')
utils.plot_slope(numpy.array([numpy.mean(real_team_tefforts_all)-delta, numpy.mean(remixed_team_tefforts_all)]), real_team_tefforts_all, real_team_scores_all, 'b:')

# Add legend and labels
matplotlib.pyplot.legend(["Individuals", "True Teams", "Nominal Teams"])
matplotlib.pyplot.xlabel("Total Submissions (Normalized)")
matplotlib.pyplot.ylabel("Quality of Best Solution (Normalized)")

# Show results
matplotlib.pyplot.show()
