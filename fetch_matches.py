""" Downloads matches from NFL site """
import sys
import os
import urllib.request
import bs4
import json

# Div class of team scores
MATCH_DIV_CLASS = 'nfl-c-matchup-strip__game'

# Class name of match's team names
MATCH_NAME_CLASS = "nfl-c-matchup-strip__team-fullname"

# Class name of match's scores
MATCH_SCORE_CLASS = "nfl-c-matchup-strip__team-score"

# URL to fetch data from
# URL_TEMPLATE = 'http://www.nfl.com/schedules/%s/REG%s'
URL_TEMPLATE = 'http://www.nfl.com/api/lazy/load?json=%s'


# Output filename for season and week data
OUTPUT_FILE_TEMPLATE = 'seasons/%s/week_%s.txt'


def fetch_page(season, week):
    """ Downloads page """
    # url = URL_TEMPLATE % (season, week)
    payload = {
        "Name": "Schedules",
        "Module": {
            "seasonFromUrl": int(season),
            "SeasonType": "REG%s" % week,
            "WeekFromUrl": 4,
            "HeaderCountryCode": "US",
            "PreSeasonPlacement": 0,
            "RegularSeasonPlacement": 0,
            "PostSeasonPlacement": 0,
            "TimeZoneID": "America/New_York"
        },
    }
    url = URL_TEMPLATE % json.dumps(payload, separators=(",", ":"))

    response = urllib.request.urlopen(url)
    code = response.getcode()
    if code != 200:
        sys.stderr.write("HTTP error %s: Failed to load page %s\n" % (code, url))
        raise IOError
    return response.read()


def create_match_doc(season, week):
    """ Creates match document from downloading page """
    results = ''

    # Download page
    html = bs4.BeautifulSoup(fetch_page(season, week), 'html.parser')

    # Fetch match divs
    match_divs = html.find_all('div', class_=MATCH_DIV_CLASS)
    team_set = set()
    if not match_divs:
        sys.stderr.write("Error, no matches found!\n")

    for match_div in match_divs:
        loser_no = 0
        loser = False
        teams = []
        scores = []

        # Get team names
        team_name_spans = match_div.find_all("span", class_=MATCH_NAME_CLASS)
        for team_name_span in team_name_spans:
            teams.append(team_name_span.string.strip())

        # Get team scores
        team_score_divs = match_div.find_all("div", class_=MATCH_SCORE_CLASS)
        for team_score_div in team_score_divs:
            scores.append(int(team_score_div.string.strip()))

        if scores:
            if scores[0] > scores[1]:
                loser_no = 1
                loser = True
            elif scores[0] < scores[1]:
                loser_no = 0
                loser = True
            else:
                loser = False

        team_tuple = (teams[0], teams[1])
        if not(team_tuple in team_set):
            team_set.add(team_tuple)
            if loser:
                results += '%s, %s, %s\n' % (
                    teams[0], teams[1], teams[1-loser_no]
                )
            else:
                results += '%s, %s\n' % (teams[0], teams[1])

    return results


def process_matches(season, week):
    """ Downloads data and saves to file """
    # Download data and generate output text
    output = create_match_doc(season, week)

    print('Processing season %s, #%s' % (season, week))
    if not os.path.exists('seasons/'+season):
        os.makedirs('seasons/'+season)
    match_file = open(OUTPUT_FILE_TEMPLATE % (season, week), 'w')
    match_file.write(output)
    match_file.close()
    print(output)


if len(sys.argv) == 3:
    process_matches(sys.argv[1], sys.argv[2])

elif len(sys.argv) == 2:
    # Iterate over all weeks
    for i in range(0, 17):
        process_matches(sys.argv[1], str(i+1))

else:
    print('Usage:\n\tpython fetch_matches.py [season] [week]')
    exit(0)
