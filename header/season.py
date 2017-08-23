''' Season class

Data format:
    Season data is stored in path "seasons/[season name]"
    Matches for week x are saved in file "seasons/[season name]/week_[x].txt"
    In each match file, format is a list of teams as:
        [team 1], [team 2], [winning team]
    The if the match has not happened yet, the winning team can be ommitted
'''

from . import matches
from . import common


class Season(object):
    def __init__(self, context, name):
        ''' Loads season by name '''
        self.name = name
        self.context = context
        self.weeks = [matches.Week(self, x) for x in common.week_range()]

    def __str__(self):
        return 'Season '+self.name+ ':\n\t' + '\n\t'.join(map(str, self.weeks))
