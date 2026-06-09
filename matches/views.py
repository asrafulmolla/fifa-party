from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.utils import timezone
from django.core.cache import cache
from .models import Match
from venues.models import WatchVenue
from .utils import sync_matches_from_api
from collections import defaultdict


def get_synced_matches():
    """Sync matches from the World Cup 2026 API, cached for 60 seconds."""
    if not cache.get('matches_synced'):
        sync_matches_from_api()
        cache.set('matches_synced', True, 60)


def schedule(request):
    get_synced_matches()
    matches = Match.objects.all().order_by('date_bst')
    
    # Group stage
    group_matches = defaultdict(list)
    knockout_matches = defaultdict(list)
    
    for match in matches:
        if match.stage == 'GROUP':
            group_matches[match.group].append(match)
        else:
            knockout_matches[match.stage].append(match)

    stage_order = ['R32', 'R16', 'QF', 'SF', 'THIRD', 'FINAL']
    knockout_stages = [(stage, knockout_matches.get(stage, [])) for stage in stage_order if knockout_matches.get(stage)]

    # Next match for countdown
    next_match = Match.objects.filter(
        status='UPCOMING', date_bst__gte=timezone.now()
    ).order_by('date_bst').first()

    # Calculate Group Standings
    standings = {}
    for group, grp_matches in group_matches.items():
        if not group:
            continue
        table = {}
        for match in grp_matches:
            # Initialize teams in the table
            if match.team1_code not in table and match.team1_code != 'TBD':
                table[match.team1_code] = {'name': match.team1_name, 'flag': match.get_team1_flag(), 'pld': 0, 'w': 0, 'd': 0, 'l': 0, 'gf': 0, 'ga': 0, 'gd': 0, 'pts': 0}
            if match.team2_code not in table and match.team2_code != 'TBD':
                table[match.team2_code] = {'name': match.team2_name, 'flag': match.get_team2_flag(), 'pld': 0, 'w': 0, 'd': 0, 'l': 0, 'gf': 0, 'ga': 0, 'gd': 0, 'pts': 0}

            # If match is completed or live, update stats
            if match.status in ['COMPLETED', 'LIVE'] and match.team1_score is not None and match.team2_score is not None:
                t1 = table.get(match.team1_code)
                t2 = table.get(match.team2_code)
                
                if t1 and t2:
                    t1['pld'] += 1
                    t2['pld'] += 1
                    t1['gf'] += match.team1_score
                    t1['ga'] += match.team2_score
                    t2['gf'] += match.team2_score
                    t2['ga'] += match.team1_score
                    
                    if match.team1_score > match.team2_score:
                        t1['w'] += 1
                        t1['pts'] += 3
                        t2['l'] += 1
                    elif match.team2_score > match.team1_score:
                        t2['w'] += 1
                        t2['pts'] += 3
                        t1['l'] += 1
                    else:
                        t1['d'] += 1
                        t2['d'] += 1
                        t1['pts'] += 1
                        t2['pts'] += 1
                        
        # Calculate Goal Difference and sort
        for code, data in table.items():
            data['gd'] = data['gf'] - data['ga']
            
        # Sort by Points (desc), Goal Difference (desc), Goals For (desc)
        sorted_table = sorted(table.values(), key=lambda x: (x['pts'], x['gd'], x['gf']), reverse=True)
        standings[group] = sorted_table

    return render(request, 'matches/schedule.html', {
        'group_matches': dict(sorted(group_matches.items())),
        'knockout_stages': knockout_stages,
        'next_match': next_match,
        'has_knockouts': bool(knockout_matches),
        'standings': dict(sorted(standings.items())),
        'page_title': 'Match Schedule | FIFA Party Bangladesh',
    })


def match_detail(request, match_id):
    get_synced_matches()
    match = get_object_or_404(Match, id=match_id)
    venues = WatchVenue.objects.filter(venue_matches__match=match).distinct()
    return render(request, 'matches/detail.html', {
        'match': match,
        'venues': venues,
        'page_title': f'{match.team1_name} vs {match.team2_name} | FIFA Party',
    })


def live_scores(request):
    """AJAX endpoint for live scores."""
    get_synced_matches()
    live = list(Match.objects.filter(status='LIVE').values(
        'id', 'team1_name', 'team2_name', 'team1_score', 'team2_score', 'status'
    ))
    upcoming = list(Match.objects.filter(
        status='UPCOMING', date_bst__gte=timezone.now()
    ).order_by('date_bst').values(
        'id', 'team1_name', 'team2_name', 'date_bst', 'status'
    )[:3])
    
    next_match = None
    if upcoming:
        nm = upcoming[0]
        nm['date_bst'] = nm['date_bst'].isoformat()
        next_match = nm

    return JsonResponse({
        'live': live,
        'next_match': next_match,
    })
