''' Manager of lists of teams and loaded seasons '''
from . import team
from . import season


class Context(object):
    def __init__(self, seasons=[]):
        ''' Loads team names and optionally seasons '''
        # Load teams from file
        with open('teams.txt', 'r') as team_file:
            team_list = [team.Team.load_record(x) for x in team_file]
            self.teams = {t.mascot: t for t in team_list}

        # Load seasons
        self.seasons = {s: season.Season(self, s) for s in seasons}

    def __str__(self):
        return '\n'.join([
            'Teams:',
            '\t'+'\n\t'.join( map(str, self.teams.values()) ),
            '\n\t'.join( map(str, self.seasons.values()) ),
        ])
