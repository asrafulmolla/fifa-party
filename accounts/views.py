from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum
from .models import UserProfile
from venues.models import WatchVenue
from predictions.models import Prediction


def register_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')
        supported_team = request.POST.get('supported_team', 'ARG')

        if not username or not email or not password:
            messages.error(request, 'All fields are required.')
        elif password != password2:
            messages.error(request, 'Passwords do not match.')
        elif User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        elif len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters.')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.profile.supported_team = supported_team
            user.profile.save()
            login(request, user)
            messages.success(request, f'Welcome to FIFA Party, {username}! 🎉')
            return redirect('/')

    from accounts.models import TEAM_CHOICES
    return render(request, 'accounts/register.html', {
        'team_choices': TEAM_CHOICES,
        'page_title': 'Join FIFA Party Bangladesh',
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            next_url = request.GET.get('next', '/')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'accounts/login.html', {'page_title': 'Sign In | FIFA Party'})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('/')


def profile_view(request, username):
    profile_user = get_object_or_404(User, username=username)
    profile = get_object_or_404(UserProfile, user=profile_user)
    venues = WatchVenue.objects.filter(submitted_by=profile_user)
    predictions = Prediction.objects.filter(user=profile_user).select_related('match')
    correct_predictions = predictions.filter(is_correct=True).count()
    badge_name, badge_class = profile.get_badge()

    if request.method == 'POST' and request.user == profile_user:
        supported_team = request.POST.get('supported_team', profile.supported_team)
        bio = request.POST.get('bio', profile.bio)
        avatar = request.FILES.get('avatar')
        profile.supported_team = supported_team
        profile.bio = bio
        if avatar:
            profile.avatar = avatar
        profile.save()
        messages.success(request, 'Profile updated!')
        return redirect('profile', username=username)

    from accounts.models import TEAM_CHOICES
    return render(request, 'accounts/profile.html', {
        'profile_user': profile_user,
        'profile': profile,
        'venues': venues,
        'predictions': predictions,
        'correct_predictions': correct_predictions,
        'badge_name': badge_name,
        'badge_class': badge_class,
        'team_choices': TEAM_CHOICES,
        'page_title': f'{username} | FIFA Party Profile',
        'is_own_profile': request.user == profile_user,
    })


def leaderboard_view(request):
    top_fans = UserProfile.objects.select_related('user').order_by('-fan_score')[:50]
    top_predictors = UserProfile.objects.select_related('user').filter(
        user__predictions__is_correct=True
    ).distinct().order_by('-fan_score')[:20]

    return render(request, 'accounts/leaderboard.html', {
        'top_fans': top_fans,
        'page_title': 'Fan Leaderboard | FIFA Party',
    })
