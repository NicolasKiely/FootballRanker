""" Week and match listing class """
from typing import List
from typing import Optional

from header import common
from header import ranking


class Match(object):
    """ Represents a match between two teams """
    def __init__(self, week: "Week", team_list: List[common.TeamName]):
        self.week: Week = week
        if len(team_list) == 2:
            played = False
            winner = None
            teams = team_list

        elif len(team_list) == 3:
            played = True
            winner = team_list[2]
            teams = team_list[:2]
            self.first_winner: bool = (self.winner == team_list[0])
            self.loser: common.TeamName = team_list[
                1 if self.first_winner else 0
            ]

        else:
            raise Exception("Bad match list: "+str(team_list))
        self.played: bool = played
        self.winner: Optional[common.TeamName] = winner
        self.teams: List[common.TeamName] = teams

    def __str__(self):
        if self.played:
            if self.first_winner:
                return '[%s], %s' % (self.teams[0], self.teams[1])
            else:
                return '%s, [%s]' % (self.teams[0], self.teams[1])
        else:
            return '%s, %s' % (self.teams[0], self.teams[1])

    @property
    def model_match_record(
            self
    ) -> common.ModelMatchRecord:
        """ Serializes match to tuple """
        return (
            self.week.num, self.teams[0], self.teams[1],
            (1 if self.first_winner else -1) if self.played else 0
        )


class Week(object):
    """ Represents a week in a season """
    def __init__(self, season, week_num: common.WeekID, load: bool = True):
        self.season = season
        self.num: common.WeekID = week_num

        # Create uninitialize ranking
        self.ranking: ranking.Ranking = ranking.Ranking(
            self.season.context, self
        )
        if not load:
            return

        # Load matches from file
        file_name = common.MATCH_FILE % (season.name, str(week_num))
        with open(file_name, 'r') as match_file:
            self.matches: List[Match] = [
                Match(self, common.parse(m)) for m in match_file
            ]

    def __str__(self):
        return 'Week: %s%s' % (
            self.num, ''.join(['\n\t\t'+str(m) for m in self.matches])
        )
