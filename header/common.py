""" Common definitions in scripts """
from typing import Tuple
from typing import NewType

# Season ID
SeasonID = NewType("SeasonName", str)

# Week numerical ID
WeekID = NewType("WeekID", int)

# Starting week
PRELIM_WEEK_ID = WeekID(0)

# Name of team
TeamName = NewType("TeamName", str)

# Match record format
ModelMatchRecord = Tuple[WeekID, TeamName, TeamName, int]

# Output filename for season and week data
MATCH_FILE = 'seasons/%s/week_%s.txt'

# Filename for team rankings at a given week in a season
RANK_FILE = 'seasons/%s/rank_%s.txt'

# Starting week number
MIN_WEEK = 1

# Last week number
MAX_WEEK = 17


def parse(record):
    """ Parses text record string, which are comma separated lines """
    return [f.strip() for f in record.split(',')]


def week_range():
    """ Returns range of weeks """
    return range(MIN_WEEK, MAX_WEEK+1)
