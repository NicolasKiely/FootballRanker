""" Calculates and saves ranking of teams for a given season """
import sys
import header.context
import header.common


argc = len(sys.argv)
if argc != 2 and argc != 3:
    print 'Usage:\n\tpython ranker.py [season] [optional previous season]'
    exit(0)

# Load season(s)
season_name = sys.argv[1]
prev_season_name = None
if argc == 2:
    ctx_seasons = [season_name]
else:
    prev_season_name = sys.argv[2]
    ctx_seasons = [prev_season_name, season_name]

ctx = header.context.Context(ctx_seasons)
season = ctx.seasons[season_name]


# Set initial scores
if argc == 2:
    # Just use 1.0
    initial_scores = {tname: 1.0 for tname, team in ctx.teams.iteritems()}

else:
    prev_season = ctx.seasons[prev_season_name]
    last_ranking = prev_season.weeks[-1].ranking

    last_ranking.load()
    initial_scores = last_ranking.score

# Calculate rankings
season.calculate_rankings(initial_scores)

# Save rankings
season.save_rankings()
