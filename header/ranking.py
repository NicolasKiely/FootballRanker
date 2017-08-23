''' Tracks ranking of teams '''

from . import common


class Ranking(object):
    ''' Ranks of all teams updated to the week '''
    def __init__(self, context, week):
        self.context = context
        self.week = week
        self.score = {tname: None for tname in context.teams.keys()}

    def calculate(self, prev_scores):
        ''' Calculate scores for this week using data from past week '''
        self.score = {k:v for k,v in prev_scores.iteritems()}
        for match in self.week.matches:
            if match.played:
                try:
                    # Fetch old scores
                    winner_score = prev_scores[match.winner]
                    loser_score = prev_scores[match.loser]

                    # Update this ranking's scores
                    score_delta = loser_score * 0.1
                    self.score[match.winner] = winner_score + score_delta
                    self.score[match.loser] = loser_score - score_delta

                except Exception as ex:
                    print ex
                    raise Exception(
                        'Error in calculating score for week %s: "%s" vs "%s"' %
                        (self.week.num, match.winner, match.loser)
                    )


    def save(self):
        ''' Saves ranking to file '''
        file_name = common.RANK_FILE %(self.week.season.name, self.week.num)
        with open(file_name, 'w') as rank_file:
            for team, score in self.score.iteritems():
                rank_file.write('%s,%s\n' % (team, score))