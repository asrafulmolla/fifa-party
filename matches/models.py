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
    ('IRN', 'Iran'), ('SAU', 'Saudi Arabia'), ('TBD', 'TBD'),
    ('RSA', 'South Africa'), ('CZE', 'Czechia'), ('BIH', 'Bosnia and Herzegovina'),
    ('QAT', 'Qatar'), ('SUI', 'Switzerland'), ('HAI', 'Haiti'),
    ('SCO', 'Scotland'), ('PAR', 'Paraguay'), ('TUR', 'Türkiye'),
    ('CUW', 'Curaçao'), ('CIV', "Côte d'Ivoire"), ('ECU', 'Ecuador'),
    ('SWE', 'Sweden'), ('TUN', 'Tunisia'), ('EGY', 'Egypt'),
    ('NZL', 'New Zealand'), ('CPV', 'Cape Verde'), ('IRQ', 'Iraq'),
    ('NOR', 'Norway'), ('ALG', 'Algeria'), ('AUT', 'Austria'),
    ('JOR', 'Jordan'), ('COD', 'DR Congo'), ('UZB', 'Uzbekistan'),
    ('COL', 'Colombia'), ('CRO', 'Croatia'), ('PAN', 'Panama'),
    ('OTHER', 'Other'),
]

STAGE_CHOICES = [
    ('GROUP', 'Group Stage'),
    ('R32', 'Round of 32'),
    ('R16', 'Round of 16'),
    ('QF', 'Quarterfinal'),
    ('SF', 'Semifinal'),
    ('THIRD', 'Third Place'),
    ('FINAL', 'Final'),
]

STATUS_CHOICES = [
    ('UPCOMING', 'Upcoming'),
    ('LIVE', 'Live'),
    ('COMPLETED', 'Completed'),
    ('POSTPONED', 'Postponed'),
]

COUNTRY_FLAG_CODES = {
    'ARG': 'ar', 'BRA': 'br', 'FRA': 'fr', 'ENG': 'gb-eng',
    'GER': 'de', 'ESP': 'es', 'POR': 'pt', 'NED': 'nl',
    'ITA': 'it', 'BEL': 'be', 'URU': 'uy', 'MEX': 'mx',
    'USA': 'us', 'CAN': 'ca', 'MAR': 'ma', 'SEN': 'sn',
    'NGR': 'ng', 'GHA': 'gh', 'JPN': 'jp', 'KOR': 'kr',
    'AUS': 'au', 'IRN': 'ir', 'SAU': 'sa', 'KSA': 'sa', 'TBD': 'un',
    'RSA': 'za', 'CZE': 'cz', 'BIH': 'ba', 'QAT': 'qa',
    'SUI': 'ch', 'HAI': 'ht', 'SCO': 'gb-sct', 'PAR': 'py',
    'TUR': 'tr', 'CUW': 'cw', 'CIV': 'ci', 'ECU': 'ec',
    'SWE': 'se', 'TUN': 'tn', 'EGY': 'eg', 'NZL': 'nz',
    'CPV': 'cv', 'IRQ': 'iq', 'NOR': 'no', 'ALG': 'dz',
    'AUT': 'at', 'JOR': 'jo', 'COD': 'cd', 'UZB': 'uz',
    'COL': 'co', 'CRO': 'hr', 'PAN': 'pa', 'OTHER': 'un',
}


class Match(models.Model):
    match_id = models.IntegerField(unique=True, null=True, blank=True)  # from football-data.org
    team1_code = models.CharField(max_length=10, choices=TEAM_CHOICES, default='TBD')
    team2_code = models.CharField(max_length=10, choices=TEAM_CHOICES, default='TBD')
    team1_name = models.CharField(max_length=100, default='TBD')
    team2_name = models.CharField(max_length=100, default='TBD')
    group = models.CharField(max_length=5, blank=True)  # 'A', 'B', ... or blank for knockouts
    stage = models.CharField(max_length=10, choices=STAGE_CHOICES, default='GROUP')
    date_bst = models.DateTimeField()  # Bangladesh Standard Time
    stadium = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='UPCOMING')
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date_bst']

    def get_team1_flag(self):
        return COUNTRY_FLAG_CODES.get(self.team1_code, 'un')

    def get_team2_flag(self):
        return COUNTRY_FLAG_CODES.get(self.team2_code, 'un')

    def score_display(self):
        if self.team1_score is not None and self.team2_score is not None:
            return f"{self.team1_score} – {self.team2_score}"
        return "vs"

    def __str__(self):
        return f"{self.team1_name} vs {self.team2_name} ({self.date_bst.strftime('%b %d')})"
