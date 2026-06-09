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

    return render(request, 'matches/schedule.html', {
        'group_matches': dict(sorted(group_matches.items())),
        'knockout_stages': knockout_stages,
        'next_match': next_match,
        'has_knockouts': bool(knockout_matches),
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
