""" Module for creating Model Data classes """
import json
from typing import List, Tuple

from modeling.team_elo_blackbox.model import ModelData


class ModelFactory(object):
    """ Factory class to serialize and create new models from data """
    __slots__ = ['_num_periods', '_teams', '_seasonal_matches']

    def __init__(
            self, num_periods: int, teams: List[str],
            seasonal_matches: List[Tuple[int, str, str, int]]
    ):
        """ Initializes with fixed args to pass to ModelData """
        self._num_periods = num_periods
        self._teams = teams
        self._seasonal_matches = seasonal_matches

    def create_blank_model(self) -> ModelData:
        """ Creates and returns new default model instance """
        elo_initial_vars = [(t, 1.0) for t in self._teams]
        elo_k = 0.05
        elo_k_decay = 0.0

        model_data = ModelData(
            self._num_periods, self._teams, self._seasonal_matches,
            elo_initial_vars, elo_k, elo_k_decay
        )
        return model_data

    @classmethod
    def serialize_model(cls, model_data: ModelData) -> str:
        """ Serializes model to json string """
        model_dict = {
            'elo_k_val': model_data.elo_k_val,
            'elo_k_decay_val': model_data.elo_k_decay_val,
            'elo_initial_vals': [
                (t, x) for t, x in model_data.elo_initial_vars.items()
            ]
        }
        return json.dumps(model_dict)
