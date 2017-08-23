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
scores = {tname: 1.0 for tname, team in ctx.teams.iteritems()}

for week in season.weeks:
    # For each week
    print 'Week #%s' % (week.num, )

    # Get match data
    for match in week.matches:
        if not match.played:
            continue

        # Fetch weeks scores for winner and loser team
        winner_score = scores[match.winner]
        loser_score = scores[match.loser]

        # Update scores for winner and loser
        score_delta = loser_score * 0.1
        scores[match.winner] = winner_score + score_delta
        scores[match.loser] = loser_score - score_delta

    # Write out scores
    rank_file_name = header.common.RANK_FILE % (season_name, week.num)
    with open(rank_file_name, 'w') as rank_file:
        for team, score in scores.iteritems():
            print '\t%s:   \t%s' % (team, score)
            rank_file.write('%s,%s\n' % (team, score))
    
#print ctx.seasons[season]
