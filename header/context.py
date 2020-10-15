""" Manager of lists of teams and loaded seasons """
from typing import Dict

from header import team
from header import season


class Context(object):
    """ Holds top level season and team data """
    def __init__(self, seasons=None):
        """ Loads team names and optionally seasons """
        if seasons is None:
            seasons = []
        # Load teams from file
        with open('teams.txt', 'r') as team_file:
            team_list = [team.Team.load_record(x) for x in team_file]
            self.teams: Dict[str, team.Team] = {
                t.mascot: t for t in team_list
            }

        # Load seasons
        self.seasons: Dict[str, season.Season] = {
            s: season.Season(self, s) for s in seasons
        }

    def __str__(self):
        return '\n'.join([
            'Teams:',
            '\t'+'\n\t'.join(map(str, self.teams.values())),
            '\n\t'.join(map(str, self.seasons.values())),
        ])
