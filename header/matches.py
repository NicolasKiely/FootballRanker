''' Week and match listing class '''

from . import common


class Match(object):
    ''' Represents a match between two teams '''
    def __init__(self, week, team_list):
        if len(team_list) == 2:
            self.played = False
            self.winner = None
            self.teams = team_list

        elif len(team_list) == 3:
            self.played = True
            self.winner = team_list[2]
            self.teams = team_list[:2]
            self.first_winner = (self.winner==team_list[0])
            self.loser = team_list[1 if self.first_winner else 0]

        else:
            raise Exception("Bad match list: "+str(team_list))

    def __str__(self):
        if self.played:
            if self.first_winner:
                return '['+ self.teams[0] +'], '+ self.teams[1]
            else:
                return self.teams[0] +', ['+ self.teams[1] +']'
        else:
            return self.teams[0] +', '+ self.teams[1]
    

class Week(object):
    ''' Represents a week in a season '''
    def __init__(self, season, week_num):
        self.season = season
        self.num = week_num

        # Load matches from file
        file_name = common.MATCH_FILE % (season.name, str(week_num))
        with open(file_name, 'r') as match_file:
            self.matches = [Match(self, common.parse(m)) for m in match_file]

    def __str__(self):
        return 'Week: '+ str(self.num) + ''.join(['\n\t\t'+str(m) for m in self.matches])
