""" Module for creating Model Data classes """
from typing import List, Tuple


class ModelFactory(object):
    """ Factory class to create new models from data """
    __slots__ = ['_num_periods', '_teams', '_seasonal_matches']

    def __init__(
            self, num_periods: int, teams: List[str],
            seasonal_matches: List[Tuple[int, str, str, int]]
    ):
        """ Initializes with fixed args to pass to ModelData """
        self._num_periods = num_periods
        self._teams = teams
        self._seasonal_matches = seasonal_matches
