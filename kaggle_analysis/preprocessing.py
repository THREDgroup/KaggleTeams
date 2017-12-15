import numpy
import csv
import pkg_resources


# Define function for loading data
def load_csv(csv_file_name: str, number_of_columns: int) -> dict:
    d = {}
    with open(csv_file_name, "r") as f:
        the_file = csv.reader(f, delimiter=',')
        for idx, line in enumerate(the_file):
            if idx is 0:
                headings = line
            else:
                temp = {}
                for i in range(0, number_of_columns):
                    if "Id" in headings[i]:
                        try:
                            temp[headings[i]] = int(line[i])
                        except ValueError:
                            try:
                                temp[headings[i]] = int(float(line[i]))
                            except ValueError:
                                temp[headings[i]] = -1

                    elif headings[i] in ["Ranking", "Score"]:
                        temp[headings[i]] = float(line[i])
                    else:
                        temp[headings[i]] = line[i]
                d[temp["Id"]] = temp
    return d


def extract_good_teams(minimum_true_teams: int, minimum_solo_individuals: int, save_good_competitions: bool=False) -> list:
    # Load data
    submissions = load_csv(pkg_resources.resource_filename('meta_kaggle', 'Submissions.csv'), 6)
    competitions = load_csv(pkg_resources.resource_filename('meta_kaggle', 'Competitions.csv'), 2)
    users = load_csv(pkg_resources.resource_filename('meta_kaggle', 'Users.csv'), 3)
    teams = load_csv(pkg_resources.resource_filename('meta_kaggle', 'Teams.csv'), 6)
    team_memberships = load_csv(pkg_resources.resource_filename('meta_kaggle', 'TeamMemberships.csv'), 3)

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

        if real_teams > minimum_true_teams and indiv_teams > minimum_solo_individuals:
            good_competitions.append(competitions[competitionkey])

    if save_good_competitions:
        numpy.savez('good_competitions.npz', good_competitions=good_competitions)

    return good_competitions
