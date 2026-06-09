import json
import feedparser
from django.shortcuts import render
from django.http import JsonResponse
from django.conf import settings
from matches.models import Match
from venues.models import WatchVenue
from django.utils import timezone


def home(request):
    """Home page with full-screen map."""
    upcoming_match = Match.objects.filter(
        status='UPCOMING', date_bst__gte=timezone.now()
    ).order_by('date_bst').first()

    live_match = Match.objects.filter(status='LIVE').first()
    next_match = live_match or upcoming_match

    venues = WatchVenue.objects.all()
    venues_data = []
    for v in venues:
        venues_data.append({
            'id': v.id,
            'name': v.name,
            'area': v.area,
            'lat': v.latitude,
            'lng': v.longitude,
            'entry_type': v.get_entry_type_display(),
            'entry_code': v.entry_type,
            'screen_size': v.get_screen_size_display(),
            'crowd_capacity': v.get_crowd_capacity_display(),
            'verified': v.verified,
            'submitted_by': v.submitted_by.username,
            'rating': round(v.community_rating, 1),
            'rating_count': v.rating_count,
            'photo': v.photo.url if v.photo else None,
            'checkin_count': v.checkin_count(),
        })

    context = {
        'google_maps_api_key': settings.GOOGLE_MAPS_API_KEY,
        'venues_json': json.dumps(venues_data),
        'next_match': next_match,
        'page_title': 'FIFA Party Bangladesh — Find Watch Party Locations',
    }
    return render(request, 'core/home.html', context)


def news(request):
    """World Cup news from RSS feeds."""
    feeds = [
        'https://feeds.bbci.co.uk/sport/football/rss.xml',
        'https://www.goal.com/feeds/en/news',
    ]
    articles = []
    for feed_url in feeds:
        try:
            feed = feedparser.parse(feed_url)
            for entry in feed.entries[:5]:
                articles.append({
                    'title': entry.get('title', ''),
                    'link': entry.get('link', ''),
                    'summary': entry.get('summary', '')[:200],
                    'published': entry.get('published', ''),
                    'source': feed.feed.get('title', 'Football News'),
                    'image': entry.get('media_thumbnail', [{}])[0].get('url', None) if entry.get('media_thumbnail') else None,
                })
        except Exception:
            pass

    context = {
        'articles': articles,
        'page_title': 'World Cup News | FIFA Party Bangladesh',
    }
    return render(request, 'core/news.html', context)


def venues_json(request):
    """AJAX endpoint for map venues."""
    match_id = request.GET.get('match_id')
    entry_filter = request.GET.get('entry', '')
    verified_only = request.GET.get('verified', '') == '1'

    venues = WatchVenue.objects.all()
    if verified_only:
        venues = venues.filter(verified=True)
    if entry_filter == 'free':
        venues = venues.filter(entry_type='FREE')
    if match_id:
        venues = venues.filter(venue_matches__match_id=match_id)

    data = []
    for v in venues:
        data.append({
            'id': v.id,
            'name': v.name,
            'area': v.area,
            'lat': v.latitude,
            'lng': v.longitude,
            'entry_type': v.get_entry_type_display(),
            'entry_code': v.entry_type,
            'screen_size': v.get_screen_size_display(),
            'crowd_capacity': v.get_crowd_capacity_display(),
            'verified': v.verified,
            'submitted_by': v.submitted_by.username,
            'rating': round(v.community_rating, 1),
            'photo': v.photo.url if v.photo else None,
            'checkin_count': v.checkin_count(),
        })
    return JsonResponse({'venues': data})
