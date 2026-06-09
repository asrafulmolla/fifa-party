from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import WatchVenue, VenueMatch, CheckIn
from matches.models import Match
from notifications.models import Notification


def venue_list(request):
    venues = WatchVenue.objects.all().select_related('submitted_by')
    return render(request, 'venues/list.html', {
        'venues': venues,
        'page_title': 'All Watch Venues | FIFA Party',
    })


def venue_detail(request, venue_id):
    venue = get_object_or_404(WatchVenue, id=venue_id)
    venue_matches = VenueMatch.objects.filter(venue=venue).select_related('match')
    user_checkins = []
    if request.user.is_authenticated:
        user_checkins = list(CheckIn.objects.filter(
            user=request.user, venue_match__venue=venue
        ).values_list('venue_match__match_id', flat=True))

    context = {
        'venue': venue,
        'venue_matches': venue_matches,
        'user_checkins': user_checkins,
        'page_title': f'{venue.name} | FIFA Party',
    }
    return render(request, 'venues/detail.html', context)


@login_required
def add_venue(request):
    matches = Match.objects.filter(status__in=['UPCOMING', 'LIVE']).order_by('date_bst')

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        address = request.POST.get('address', '').strip()
        area = request.POST.get('area', '').strip()
        latitude = request.POST.get('latitude', '').strip()
        longitude = request.POST.get('longitude', '').strip()
        entry_type = request.POST.get('entry_type', 'FREE')
        entry_fee_details = request.POST.get('entry_fee_details', '')
        screen_size = request.POST.get('screen_size', 'BIG')
        crowd_capacity = request.POST.get('crowd_capacity', 'MEDIUM')
        contact_info = request.POST.get('contact_info', '')
        selected_matches = request.POST.getlist('matches')
        photo = request.FILES.get('photo')

        if not name or not address or not area or not latitude or not longitude:
            messages.error(request, 'Please fill in all required fields.')
        else:
            try:
                venue = WatchVenue.objects.create(
                    name=name,
                    address=address,
                    area=area,
                    latitude=float(latitude),
                    longitude=float(longitude),
                    submitted_by=request.user,
                    entry_type=entry_type,
                    entry_fee_details=entry_fee_details,
                    screen_size=screen_size,
                    crowd_capacity=crowd_capacity,
                    contact_info=contact_info,
                    photo=photo,
                )
                for match_id in selected_matches:
                    try:
                        match = Match.objects.get(id=match_id)
                        VenueMatch.objects.create(venue=venue, match=match)
                    except Match.DoesNotExist:
                        pass

                # Award fan score
                profile = request.user.profile
                profile.fan_score += 10
                profile.save()

                Notification.objects.create(
                    user=request.user,
                    notification_type='GENERAL',
                    title='Venue Submitted!',
                    message=f'Your venue "{name}" has been added to the map. +10 Fan Points!',
                    link=f'/venues/{venue.id}/',
                )

                messages.success(request, f'"{name}" added to the map! You earned +10 Fan Points!')
                return redirect('venue_detail', venue_id=venue.id)
            except ValueError:
                messages.error(request, 'Invalid coordinates. Please use the map pin.')

    return render(request, 'venues/add.html', {
        'matches': matches,
        'page_title': 'Add Watch Venue | FIFA Party',
    })


@login_required
@require_POST
def toggle_checkin(request):
    venue_match_id = request.POST.get('venue_match_id')
    venue_match = get_object_or_404(VenueMatch, id=venue_match_id)

    checkin, created = CheckIn.objects.get_or_create(
        user=request.user,
        venue_match=venue_match,
    )
    if not created:
        checkin.delete()
        action = 'removed'
    else:
        action = 'added'
        # Award fan score
        profile = request.user.profile
        profile.fan_score += 1
        profile.save()
        # Award venue owner
        owner_profile = venue_match.venue.submitted_by.profile
        owner_profile.fan_score += 2
        owner_profile.save()

    checkin_count = venue_match.checkin_set.count()
    return JsonResponse({
        'action': action,
        'checkin_count': checkin_count,
    })
