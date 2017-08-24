''' Downloads matches from NFL site '''

import sys
import os
import urllib2
import bs4

# Div class of team scores
MATCH_DIV_CLASS = 'list-matchup-row-team'

# URL to fetch data from
URL_TEMPLATE = 'http://www.nfl.com/schedules/%s/REG%s'

# Output filename for season and week data
OUTPUT_FILE_TEMPLATE = 'seasons/%s/week_%s.txt'


def fetch_page(season, week):
    ''' Downloads page '''
    url = URL_TEMPLATE % (season, week)

    response = urllib2.urlopen(url)
    return response.read()


def create_match_doc(season, week):
    ''' Creates match document from downloading page '''
    results = ''

    # Download page
    html = bs4.BeautifulSoup(fetch_page(season, week), 'html.parser')

    # Fetch match divs
    match_divs = html.find_all('div', class_=MATCH_DIV_CLASS)
    for match_div in match_divs:
        field_no = 0
        loser_no = 0 
        loser = False
        teams = []
        for field_div in match_div.children:
            if not(type(field_div) is bs4.element.Tag):
                continue

            fclass = field_div['class']
            if 'team-name' in fclass:
                teams.append(field_div.contents[0])

                if 'lost' in fclass:
                    loser = True
                    loser_no = field_no

                field_no += 1

        if loser:
            results += '%s, %s, %s\n' % (teams[0], teams[1], teams[1-loser_no])
        else:
            results += '%s, %s\n' % (teams[0], teams[1])

    return results


def process_matches(season, week):
    ''' Downloads data and saves to file '''
    # Download data and generate output text
    output = create_match_doc(season, week)

    print 'Processing season %s, #%s' % (season, week)
    if not os.path.exists('seasons/'+season):
        os.makedirs('seasons/'+season)
    match_file = open(OUTPUT_FILE_TEMPLATE % (season, week), 'w')
    match_file.write(output)
    match_file.close()
    print output

if len(sys.argv) == 3:
    season = sys.argv[1]
    week = sys.argv[2]
    process_matches(season, week)

elif len(sys.argv) == 2:
    # Iterate over all weeks
    season = sys.argv[1]
    for week in range(0, 17):
        process_matches(season, str(week+1))

else:
    print 'Usage:\n\tpython fetch_matches.py [season] [week]'
    exit(0)
    
