''' Lists out season's picks for season. Add bb to use formatted code '''

import sys
import header.context
import header.common

plain_messages = {
    'week_num': 'Week: %s',
    'pick': 'Pick: %s',
    'owned': 'Owned Teams:',
    'score': 'Week Score: %s',
    'proj_pre': '',
    'proj_owned': 'Projected Owned Teams:',
    'proj_score': 'Projected Week Score: %s',
    'proj_post': '',
    'begin': '',
    'end': ''
}

formatted_messages = {
    'week_num': '[b]Week[/b]: %s',
    'pick': '[u]Pick[/u]: %s',
    'owned': '[u]Owned Teams[/u]:',
    'score': '[u]Week Score[/u]: %s',
    'proj_pre': '[color=gray]',
    'proj_owned': '[u]Projected Owned Teams[/u]:',
    'proj_score': '[u]Projected Week Score[/u]: %s',
    'proj_post': '[/color]',
    'begin': ' to lose.\n\n[font=Courier New][b]The Plan: Week [/b][/font]\n[spoiler]',
    'end': '[/spoiler]'
}

argc = len(sys.argv)
if argc != 2 and argc != 3:
    print 'Usage:\n\tpython picker.py [season]'
    exit(0)

txt = formatted_messages if argc==3 else plain_messages



# Load season
season_name = sys.argv[1]
ctx = header.context.Context([season_name])
season = ctx.seasons[season_name]
season.load_rankings()

# Set of teams to pick and teams won
available_teams = set(ctx.teams.keys())
owned_teams = set()
team_points = {t:0 for t in ctx.teams.keys()}

# Projected stats
proj_owned_teams = set()
proj_team_points = {t:0 for t in ctx.teams.keys()}

print txt['begin']
for week in season.weeks:
    # For each week
    print txt['week_num'] % week.num
    all_matches_played = True

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

        # Get the lower and higher ranked teams
        lteam, hteam = match.teams
        lscore, hscore = standing.score[lteam], standing.score[hteam]
        if lscore > hscore:
            lteam, hteam = hteam, lteam
            lscore, hscore = hscore, lscore

        # Update team points
        if match.played:
            team_points[match.winner] += 1
            proj_team_points[match.winner] += 1
        else:
            # Guess that better ranked team wins
            proj_team_points[hteam] += 1
            all_matches_played = False
            

        # Update best team to pick
        if lteam in available_teams:
            if (best_team == None) or (lscore > best_score):
                best_team = lteam
                best_score = lscore
                best_match = match
                

    # Evaluate best team pick
    print txt['pick'] % best_team,
    if best_match.played:
        if best_match.loser==best_team:
            print ' [Pick Aqcuired]'
            available_teams.remove(best_team)
            owned_teams.add(best_team)
            proj_owned_teams.add(best_team)

        else:
            print ' [Pick Discarded]'
    else:
        # This is a projection
        available_teams.remove(best_team)
        proj_owned_teams.add(best_team)
        print

    # List team score status
    print txt['owned'] +'\n    ',
    week_score = 0
    for team in owned_teams:
        week_score += team_points[team]
        print '%s [%s],' % (team, team_points[team]),
    print '\n'+ txt['score']  % week_score
    print
    
    if not all_matches_played:
        print txt['proj_pre'],
        print txt['proj_owned'] +'\n    ',
        proj_score = 0
        for team in proj_owned_teams:
            proj_score += proj_team_points[team]
            print '%s [%s],' % (team, proj_team_points[team]),

        print '\n'+ txt['proj_score'] % proj_score
        print txt['proj_post']

print txt['end']
