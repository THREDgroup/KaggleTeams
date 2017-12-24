import numpy
import csv
import pkg_resources
import os
import requests
import zipfile
import io


# Check the setup
def check_setup() -> None:
    if not os.path.exists('./meta_kaggle/'):
        os.mkdir('meta_kaggle')
        os.chdir('./meta_kaggle')
        zip_file_url = "https://storage.googleapis.com/kaggle-datasets/9/167/meta-kaggle.zip?GoogleAccessId=web-data@kaggle-161607.iam.gserviceaccount.com&Expires=1514347854&Signature=KUUd9GSjps2JYGGBIvlg794%2FdJU54kqqHqxiDs1GqKTuJYgRpp86axurm2PS44DlNzYoXqofZ09atAvZjaEkL2JMfJyZnmC0fj0n%2FCa%2Bflb%2FdtzbYpiUrZqrP%2FZ94LPqn%2FtR538lPxVA%2BXP4fWYjs9qUuv8Hl7xQLgWYNdavve3pcrVAQbYqfzVjigWeAvL5jTGnXoOCl81qzVKwEmtt8mrWekmHF%2FA1tMoVjrkMnZUb62bzKpqIo%2BPVxQivMet%2F%2Fxxo237Slc4WrqOL0zmpe759W9ysybUFfA42zAVFZ4BF0f1jW%2BmaJKemXTUc4xF2w6HeTayBTFRXBBvjlxdCtg%3D%3D"
        r = requests.get(zip_file_url)
        z = zipfile.ZipFile(io.BytesIO(r.content))
        z.extractall()
        os.chdir('..')
    if not os.path.exists('./meta_kaggle/__init__.py'):
        open('./meta_kaggle/__init__.py', 'a').close()


# Define function for loading data
def load_csv(csv_file_name: str, number_of_columns: int) -> dict:
    csv_file_path = pkg_resources.resource_filename('meta_kaggle', csv_file_name)
    d = {}
    with open(csv_file_path, "r") as f:
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
    check_setup()

    # Load data
    submissions = load_csv('Submissions.csv', 6)
    competitions = load_csv('Competitions.csv', 2)
    users = load_csv('Users.csv', 3)
    teams = load_csv('Teams.csv', 6)
    team_memberships = load_csv('TeamMemberships.csv', 3)

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
