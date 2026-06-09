from django.db import models
from django.contrib.auth.models import User

TEAM_CHOICES = [
    ('ARG', 'Argentina'), ('BRA', 'Brazil'), ('FRA', 'France'),
    ('ENG', 'England'), ('GER', 'Germany'), ('ESP', 'Spain'),
    ('POR', 'Portugal'), ('NED', 'Netherlands'), ('ITA', 'Italy'),
    ('BEL', 'Belgium'), ('URU', 'Uruguay'), ('MEX', 'Mexico'),
    ('USA', 'United States'), ('CAN', 'Canada'), ('MAR', 'Morocco'),
    ('SEN', 'Senegal'), ('NGR', 'Nigeria'), ('GHA', 'Ghana'),
    ('JPN', 'Japan'), ('KOR', 'South Korea'), ('AUS', 'Australia'),
    ('IRN', 'Iran'), ('SAU', 'Saudi Arabia'), ('OTHER', 'Other'),
]

COUNTRY_FLAG_CODES = {
    'ARG': 'ar', 'BRA': 'br', 'FRA': 'fr', 'ENG': 'gb-eng',
    'GER': 'de', 'ESP': 'es', 'POR': 'pt', 'NED': 'nl',
    'ITA': 'it', 'BEL': 'be', 'URU': 'uy', 'MEX': 'mx',
    'USA': 'us', 'CAN': 'ca', 'MAR': 'ma', 'SEN': 'sn',
    'NGR': 'ng', 'GHA': 'gh', 'JPN': 'jp', 'KOR': 'kr',
    'AUS': 'au', 'IRN': 'ir', 'SAU': 'sa', 'OTHER': 'un',
}


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    supported_team = models.CharField(max_length=10, choices=TEAM_CHOICES, default='ARG')
    fan_score = models.IntegerField(default=0)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True, max_length=300)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_flag_code(self):
        return COUNTRY_FLAG_CODES.get(self.supported_team, 'un')

    def get_badge(self):
        if self.fan_score >= 200:
            return ('World Cup Superfan', 'gold')
        elif self.fan_score >= 100:
            return ('5 Check-ins', 'silver')
        elif self.fan_score >= 10:
            return ('First Submission', 'bronze')
        return ('Fan', 'default')

    def __str__(self):
        return f"{self.user.username} – {self.get_supported_team_display()}"
