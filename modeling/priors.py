""" Calculations for handling priors """
import abc
from typing import List

from header.season import Season


class Priors:
    """ Generic class for priors """
    def __init__(self, seasons: List[Season]):
        self.seasons: List[Season] = seasons

    @abc.abstractmethod
    def calculate(self):
        """ Creates estimates of priors """


class TeamWOWPriors(Priors):
    """ Team Week over Week Priors

    Team WoW priors:
        estimate of binomial model of how likely each team is
        to win for the n'th week in a season.
    """
    def calculate(self):
        """ Runs estimation """
        # Calculate win/loss tally
        team_win_loss = {}
        for season in self.seasons:
            for week in season.weeks:
                for match in week.matches:
                    if match.winner is None:
                        continue
                    self.calculate_match(team_win_loss, week.num, match)

        # Estimate mean and variance
        team_results = {
            team_name: {
                week_num: self.calculate_binomial(*win_loss)
                for week_num, win_loss in weekly_win_loss.items()
            }
            for team_name, weekly_win_loss in team_win_loss.items()
        }

        return team_results

    @staticmethod
    def calculate_binomial(wins, total):
        """ Estimate binomial mean/n and variance/n """
        if total <= 0:
            # Default case is coin flip
            p = 0.5
        else:
            # p = probability of win
            p = wins/total
        return p, p * (1-p)



    @staticmethod
    def calculate_match(results, week_num, match):
        """ Calculate results for a given week """
        if match.winner not in results:
            # Initialize team
            results[match.winner] = {}

        if match.loser not in results:
            results[match.loser] = {}

        if week_num not in results[match.winner]:
            # Initialize week for team
            results[match.winner][week_num] = [0, 0]

        if week_num not in results[match.loser]:
            results[match.loser][week_num] = [0, 0]

        # Update winner
        results[match.winner][week_num][0] += 1
        results[match.winner][week_num][1] += 1

        # Update loser
        results[match.loser][week_num][1] += 1
