''' Lists out season's picks '''

import sys
import header.context
import header.common


if len(sys.argv) != 2:
    print 'Usage:\n\tpython picker.py [season]'
    exit(0)

# Load season
season_name = sys.argv[1]
ctx = header.context.Context([season_name])
season = ctx.seasons[season_name]
season.load_rankings()

# Set of teams to pick and teams won
available_teams = set(ctx.teams.keys())
owned_teams = set()
team_points = {t:0 for t in ctx.teams.keys()}

for week in season.weeks:
    # For each week
    print 'Week:', week.num

    # Load last standing ranking
    if week.num == 1:
        standing = season.week0.ranking
    else:
        standing = season.weeks[week.num-1].ranking

    # Best losing team
    best_team = None
    best_score = 0
    best_match = None

    for match in week.matches:
        # For each match

        if match.played:
            team_points[match.winner] += 1

        # Get the lower and higher ranked teams
        lteam, hteam = match.teams
        lscore, hscore = standing.score[lteam], standing.score[hteam]
        if lscore > hscore:
            lteam, hteam = hteam, lteam
            lscore, hscore = hscore, lscore

        # Update best team to pick
        if lteam in available_teams:
            if (best_team == None) or (lscore > best_score):
                best_team = lteam
                best_score = lscore
                best_match = match
                

    # Evaluate best team pick
    print '  Pick: '+ best_team,
    if best_match.played:
        if best_match.loser==best_team:
            print ' [Pick Aqcuired]'
            available_teams.remove(best_team)
            owned_teams.add(best_team)

        else:
            print ' [Pick Discarded]'
    else:
        print

    # List team score status
    print '    Own: ',
    week_score = 0
    for team in owned_teams:
        week_score += team_points[team]
        print '%s [%s],' % (team, team_points[team]),

    print '\n  Week Score: ', week_score
    print
