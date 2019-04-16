""" Common definitions in scripts """


# Output filename for season and week data
MATCH_FILE = 'seasons/%s/week_%s.txt'

# Filename for team rankings at a given week in a season
RANK_FILE = 'seasons/%s/rank_%s.txt'


def parse(record):
    """ Parses text record string, which are comma separated lines """
    return [f.strip() for f in record.split(',')]


def week_range():
    """ Returns range of weeks """
    return range(1, 18)
