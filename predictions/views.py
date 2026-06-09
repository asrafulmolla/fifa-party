from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Prediction, PollResponse
from matches.models import Match
from django.db.models import Count


@login_required
@require_POST
def predict(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    predicted_winner = request.POST.get('predicted_winner')
    
    if match.status != 'UPCOMING':
        return JsonResponse({'error': 'Predictions closed for this match.'}, status=400)

    prediction, created = Prediction.objects.update_or_create(
        user=request.user,
        match=match,
        defaults={'predicted_winner': predicted_winner},
    )
    return JsonResponse({
        'status': 'ok',
        'created': created,
        'predicted_winner': predicted_winner,
    })


@login_required
@require_POST
def mood_poll(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    mood = request.POST.get('mood')

    if match.status != 'COMPLETED':
        return JsonResponse({'error': 'Poll only available for completed matches.'}, status=400)

    PollResponse.objects.update_or_create(
        user=request.user,
        match=match,
        defaults={'mood': mood},
    )

    # Get poll results
    results = PollResponse.objects.filter(match=match).values('mood').annotate(count=Count('mood'))
    total = sum(r['count'] for r in results)
    poll_data = {r['mood']: round((r['count'] / total) * 100) if total else 0 for r in results}

    return JsonResponse({'status': 'ok', 'results': poll_data, 'total': total})


def poll_results(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    results = PollResponse.objects.filter(match=match).values('mood').annotate(count=Count('mood'))
    total = sum(r['count'] for r in results)
    poll_data = {r['mood']: {'count': r['count'], 'pct': round((r['count'] / total) * 100) if total else 0} for r in results}
    user_vote = None
    if request.user.is_authenticated:
        resp = PollResponse.objects.filter(user=request.user, match=match).first()
        if resp:
            user_vote = resp.mood
    return JsonResponse({'results': poll_data, 'total': total, 'user_vote': user_vote})
