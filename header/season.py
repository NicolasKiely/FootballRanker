""" Season class

Data format:
    Season data is stored in path "seasons/[season name]"
    Matches for week x are saved in file "seasons/[season name]/week_[x].txt"
    In each match file, format is a list of teams as:
        [team 1], [team 2], [winning team]
    The if the match has not happened yet, the winning team can be ommitted
"""
from typing import List

from header import matches
from header import common


class Season(object):
    def __init__(self, context, name: common.SeasonID):
        """ Loads season by name """
        self.name: common.SeasonID = name
        self.context = context
        self.week0: matches.Week = matches.Week(
            self, common.PRELIM_WEEK_ID, load=False
        )
        self.weeks: List[matches.Week] = [
            matches.Week(self, x) for x in common.week_range()
        ]

    def calculate_rankings(self, initial_score: float):
        """ Calculate rankings for all weeks """
        scores = initial_score
        self.week0.ranking.set_scores(initial_score)

        for week in self.weeks:
            # Calculate this week's rankings
            try:
                week.ranking.calculate(scores)
            except KeyError as ex:
                print(
                    "Error, could not compute ranks for week %s" % week.num
                )
                raise ex

            # Update scores for use in next week
            scores = week.ranking.score

    def load_rankings(self):
        """ Loads rankings from file """
        for week in self.weeks:
            week.ranking.load()

        self.week0.ranking.load()

    def save_rankings(self):
        """ Saves rankings to file """
        for week in self.weeks:
            week.ranking.save()

        self.week0.ranking.save()

    @property
    def model_match_records(self) -> List[common.ModelMatchRecord]:
        return [
            match.model_match_record
            for week in self.weeks
            for match in week.matches
        ]
    
    def __str__(self):
        return 'Season %s\n\t%s' % (
            self.name, '\n\t'.join(map(str, self.weeks))
        )
