""" Script to evaluate a model for a given season

Usage: python -m modeling.eval_model [season] [to_week] [model def]
"""
import csv
import datetime as dtt
import sys

import header.context
from modeling.team_elo_blackbox import factory, model


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

        csv_writer = csv.writer(sys.stdout)
        csv_writer.writerow(
            ['Week', 'Team 1 Name', 'Team 1 ELO', 'Team 2 Name', 'Team 2 ELO']
        )

        for p in model_data.periods_index:
            period_matches = model_data.period_matches_index(p)
            if len(period_matches) == 0:
                continue
            for m in period_matches:
                elo_1 = model.elo(model_data, m, m.t1)
                elo_2 = model.elo(model_data, m, m.t2)
                csv_writer.writerow([p, m.t1, elo_1, m.t2, elo_2])


if __name__ == '__main__':
    eval_model(*sys.argv[1:])
