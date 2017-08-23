''' Calculates and saves ranking of teams for a given season '''

import sys
import header.context
import header.common


if len(sys.argv) != 2:
    print 'Usage:\n\tpython ranker.py [season]'
    exit(0)

# Load season
season_name = sys.argv[1]
ctx = header.context.Context([season_name])
season = ctx.seasons[season_name]

# Set initial scores
initial_scores = {tname: 1.0 for tname, team in ctx.teams.iteritems()}

# Calculate rankings
season.calculate_rankings(initial_scores)

# Save rankings
season.save_rankings()
