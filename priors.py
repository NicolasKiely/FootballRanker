""" Computes priors for teams """
import sys
import header.context


argc = len(sys.argv)
if argc < 2:
    print('Usage:\n\tpython priors.py [season] [season] ...')
    exit(0)

# Load seasons
season_names = sorted(sys.argv[1:], key=int)
ctx = header.context.Context(season_names)

# Calculate priors
acc_seasons = []
for season_name in season_names:
    acc_seasons.append(season_name)
    season = ctx.seasons[season_name]
    season.calculate_team_priors(acc_seasons)
