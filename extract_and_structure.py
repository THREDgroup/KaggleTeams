import numpy
import utils

# Set constants
minimum_true_teams = 10
minimum_indiv_teams = 10

# Load data
submissions = utils.load_csv('./meta-kaggle/Submissions.csv', 6)
competitions = utils.load_csv('./meta-kaggle/Competitions.csv', 2)
users = utils.load_csv('./meta-kaggle/Users.csv', 3)
teams = utils.load_csv('./meta-kaggle/Teams.csv', 6)
team_memberships = utils.load_csv('./meta-kaggle/TeamMemberships.csv', 3)

# For each team make a userlist and for each competiton a teamlist
for competitionkey in competitions:
    competitions[competitionkey]["team_list"] = []
for teamkey in teams:
    teams[teamkey]["user_list"] = {}

# Assign teams to members
memberships = {}
for membershipkey in team_memberships:
    the_team = team_memberships[membershipkey]["TeamId"]
    the_user = team_memberships[membershipkey]["UserId"]
    teams[the_team]["user_list"][the_user] = 0

# Count submissions per team member
total_submissions = 0
error_submissions = 0
for submissionkey in submissions:
    the_team = submissions[submissionkey]["TeamId"]
    the_user = submissions[submissionkey]["SubmittedUserId"]
    try:
        teams[the_team]["user_list"][the_user] += 1
        total_submissions += 1
    except KeyError:
        error_submissions += 1

print(total_submissions, error_submissions)

# For each competitions, assign teams to it
for teamkey in teams:
    competition_id = teams[teamkey]["CompetitionId"]
    competitions[competition_id]["team_list"].append(teams[teamkey])

# For each team in each competition, analyze users to it
good_competitions = []
for competitionkey in competitions:
    indiv_teams = 0
    team_size = []
    real_teams = 0
    for team in competitions[competitionkey]["team_list"]:
        if len(team["user_list"]) == 1:
            indiv_teams += 1
        else:
            real_teams += 1
            team_size.append(len(team["user_list"]))

    competitions[competitionkey]["indiv_team_count"] = indiv_teams
    competitions[competitionkey]["real_team_count"] = real_teams
    competitions[competitionkey]["real_team_sizes"] = team_size

    if real_teams > minimum_true_teams and indiv_teams > minimum_indiv_teams:
        good_competitions.append(competitions[competitionkey])

numpy.savez('good_competitions.npz', good_competitions=good_competitions)

print(len(good_competitions))
