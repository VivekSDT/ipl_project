from django.http import JsonResponse
from django.db.models import Count, Sum, F, FloatField
from django.db.models.functions import Cast
from django.db.models import Q
from .models import Match, Delivery

def matches_per_year(request):
    """Return number of matches played per season (sorted ascending)."""
    qs = Match.objects.values('season').annotate(matches=Count('match_id')).order_by('season')
    data = [{'season': int(r['season']), 'matches': int(r['matches'])} for r in qs]
    return JsonResponse({'data': data})

def stacked_wins_per_team_per_year(request):
    """Return wins per team per season as a flat list. Client converts to stacked format."""
    qs = (Match.objects
          .exclude(winner__isnull=True)
          .values('season', 'winner')
          .annotate(wins=Count('match_id'))
          .order_by('season'))
    data = [{'season': int(r['season']), 'team': r['winner'], 'wins': int(r['wins'])} for r in qs]
    return JsonResponse({'data': data})

def extra_runs_per_team(request, year):
    """Extra runs conceded per bowling team in a given year."""
    qs = (Delivery.objects
          .filter(match__season=year)
          .values('bowling_team')
          .annotate(extra_runs_conceded=Sum('extra_runs'))
          .order_by('-extra_runs_conceded'))
    data = [{'team': r['bowling_team'], 'extra_runs': int(r['extra_runs_conceded'] or 0)} for r in qs]
    return JsonResponse({'data': data})

def top_economical_bowlers(request, year):
    """Top economical bowlers for season `year`.

    Economy calculation:
      economy = total_runs_conceded / (legal_balls / 6)
    where legal_balls = total deliveries - wides - noballs
    """
    deliveries = Delivery.objects.filter(match__season=year)
    qs = (deliveries.values('bowler')
          .annotate(total_runs=Sum('total_runs'), wides=Sum('wide_runs'), noballs=Sum('noball_runs'), balls=Count('id')))

    results = []
    for r in qs:
        total_runs = int(r['total_runs'] or 0)
        wides = int(r['wides'] or 0)
        noballs = int(r['noballs'] or 0)
        balls = int(r['balls'] or 0)
        legal_balls = balls - wides - noballs
        if legal_balls <= 0:
            continue
        overs = legal_balls / 6.0
        economy = total_runs / overs
        results.append({'bowler': r['bowler'], 'total_runs': total_runs, 'legal_balls': legal_balls, 'economy': round(economy, 3)})

    results_sorted = sorted(results, key=lambda x: x['economy'])[:20]
    return JsonResponse({'data': results_sorted})

def matches_played_vs_won(request, year):
    """For each team in season `year`, return matches played and matches won."""
    matches = Match.objects.filter(season=year)
    # gather unique teams
    teams1 = set(matches.values_list('team1', flat=True))
    teams2 = set(matches.values_list('team2', flat=True))
    teams = sorted(teams1.union(teams2))
    data = []
    for team in teams:
        played = matches.filter(Q(team1=team) | Q(team2=team)).count()
        won = matches.filter(winner=team).count()
        data.append({'team': team, 'played': played, 'won': won})
    return JsonResponse({'data': data})
