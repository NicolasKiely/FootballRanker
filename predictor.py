""" Makes predictions of teams """

import sys
import header.context
import header.common
from jinja2 import Template

report = Template("""{% for week in weeks %}
Week: {{ week.num }}
{%- for match in week.matches %}
{{ match.hteam }} vs {{ match.lteam }}
    Predicted winner: {{ match.hteam }}
    {%- if match.winner %}
    Actual winner: {{ match.winner }}{% endif %}
{% endfor %}
{% if week.played %}Accuracy: {{ week.correct }} / {{ week.played }}{% endif %}

{% endfor %}""")

argc = len(sys.argv)
if argc != 2 and argc != 3:
    print('Usage:\n\tpython predictor.py')
    exit(0)


# Load season
season_name = sys.argv[1]
ctx = header.context.Context([season_name])
season = ctx.seasons[season_name]
season.load_rankings()

# Set of teams to pick and teams won
available_teams = set(ctx.teams.keys())
owned_teams = set()
team_points = {t: 0 for t in ctx.teams.keys()}

# Projected stats
proj_owned_teams = set()
proj_team_points = {t: 0 for t in ctx.teams.keys()}

results = {
    'weeks': []
}

for week in season.weeks:
    # For each week
    week_results = {'num': week.num, 'matches': [], 'correct': 0, 'played': 0}
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

        match_results = {'hteam': hteam, 'lteam': lteam}

        # Update team points
        if match.played:
            team_points[match.winner] += 1
            proj_team_points[match.winner] += 1
            match_results['winner'] = match.winner
            week_results['played'] += 1
            if match.winner == hteam:
                week_results['correct'] += 1
        else:
            # Guess that better ranked team wins
            proj_team_points[hteam] += 1
            all_matches_played = False
            
        # Update best team to pick
        if lteam in available_teams:
            if (best_team is None) or (lscore > best_score):
                best_team = lteam
                best_score = lscore
                best_match = match
        week_results['matches'].append(match_results)
                
    # Evaluate best team pick
    if best_match.played:
        if best_match.loser == best_team:
            available_teams.remove(best_team)
            owned_teams.add(best_team)
            proj_owned_teams.add(best_team)

    else:
        # This is a projection
        available_teams.remove(best_team)
        proj_owned_teams.add(best_team)

    # List team score status
    week_score = 0
    for team in owned_teams:
        week_score += team_points[team]
    
    if not all_matches_played:
        proj_score = 0
        for team in proj_owned_teams:
            proj_score += proj_team_points[team]
    results['weeks'].append(week_results)

print(report.render(**results))
