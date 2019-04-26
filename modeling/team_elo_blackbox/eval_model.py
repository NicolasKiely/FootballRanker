""" Script to evaluate a model for a given season

Usage: python -m modeling.eval_model [season] [to_week] [model def]
"""
import datetime as dtt
import sys

import header.context
from modeling.team_elo_blackbox import factory


def eval_model(season: str=None, to_week: int=None, model_def_file: str=None):
    """ Evaluate model

    :param season: Season to process (defaults to last year)
    :param to_week: Week to process to (default 18)
    :param model_def_file: Name of model definition to evaluate
    """
    if season is None:
        season = str(dtt.datetime.now().year - 1)

    if to_week is None:
        to_week = 18

    ctx = header.context.Context([season])
    # Load team and season data
    teams = ctx.teams
    team_index = list(teams.keys())
    season = ctx.seasons[season]
    season_matches = season.model_match_records

    model_factory = factory.ModelFactory(to_week, team_index, season_matches)

    if model_def_file is None:
        # Use default model
        model_data = model_factory.create_blank_model()


if __name__ == '__main__':
    eval_model(*sys.argv[1:])
