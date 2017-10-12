''' Tracks ranking of teams '''

from . import common


class Ranking(object):
    ''' Ranks of all teams updated to the week '''
    def __init__(self, context, week):
        self.context = context
        self.week = week
        self.score = {tname: None for tname in context.teams.keys()}

    def set_scores(self, scores):
        ''' Sets scores for ranking '''
        self.score = {k:v for k,v in scores.iteritems()}

    def calculate(self, prev_scores):
        ''' Calculate scores for this week using data from past week '''
        self.set_scores(prev_scores)
        for match in self.week.matches:
            if match.played:
                # Fetch old scores
                winner_score = float(prev_scores[match.winner])
                loser_score = float(prev_scores[match.loser])

                # Update this ranking's scores
                score_delta = loser_score * 0.1
                self.score[match.winner] = winner_score + score_delta
                self.score[match.loser] = loser_score - score_delta


    def save(self):
        ''' Saves ranking to file '''
        file_name = common.RANK_FILE %(self.week.season.name, self.week.num)
        with open(file_name, 'w') as rank_file:
            for team, score in self.score.iteritems():
                rank_file.write('%s,%s\n' % (team, score))

    def load(self):
        ''' Loads ranking from file '''
        file_name = common.RANK_FILE %(self.week.season.name, self.week.num)
        with open(file_name, 'r') as rank_file:
            for record in rank_file:
                team, score = common.parse(record)
                self.score[team] = score
