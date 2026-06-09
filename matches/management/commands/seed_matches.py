"""
Management command to seed FIFA World Cup 2026 match data.
Run: python manage.py seed_matches
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from matches.models import Match
import pytz

# Timezones
CT = pytz.timezone('America/Chicago')  # Central Time
BST = pytz.timezone('Asia/Dhaka')      # Bangladesh Standard Time (UTC+6)

# Exact opening matchday schedule (Central Time, as requested)
GROUP_MATCHES = [
    # June 11
    {'team1': 'MEX', 'team2': 'RSA', 't1': 'Mexico', 't2': 'South Africa', 'group': 'A', 'date': '2026-06-11 14:00', 'stadium': 'Mexico City Stadium', 'city': 'Mexico City'},
    {'team1': 'KOR', 'team2': 'CZE', 't1': 'South Korea', 't2': 'Czechia', 'group': 'A', 'date': '2026-06-11 21:00', 'stadium': 'Estadio Guadalajara', 'city': 'Zapopan'},
    
    # June 12
    {'team1': 'CAN', 'team2': 'BIH', 't1': 'Canada', 't2': 'Bosnia and Herzegovina', 'group': 'B', 'date': '2026-06-12 14:00', 'stadium': 'Toronto Stadium', 'city': 'Toronto'},
    {'team1': 'USA', 'team2': 'PAR', 't1': 'United States', 't2': 'Paraguay', 'group': 'D', 'date': '2026-06-12 20:00', 'stadium': 'Los Angeles Stadium', 'city': 'Inglewood'},
    
    # June 13
    {'team1': 'QAT', 'team2': 'SUI', 't1': 'Qatar', 't2': 'Switzerland', 'group': 'B', 'date': '2026-06-13 14:00', 'stadium': 'San Francisco Bay Area Stadium', 'city': 'Santa Clara'},
    {'team1': 'BRA', 'team2': 'MAR', 't1': 'Brazil', 't2': 'Morocco', 'group': 'C', 'date': '2026-06-13 17:00', 'stadium': 'New York New Jersey Stadium', 'city': 'East Rutherford'},
    {'team1': 'HAI', 'team2': 'SCO', 't1': 'Haiti', 't2': 'Scotland', 'group': 'C', 'date': '2026-06-13 20:00', 'stadium': 'Boston Stadium', 'city': 'Foxborough'},
    {'team1': 'AUS', 'team2': 'TUR', 't1': 'Australia', 't2': 'Türkiye', 'group': 'D', 'date': '2026-06-13 23:00', 'stadium': 'BC Place Vancouver', 'city': 'Vancouver'},

    # June 14
    {'team1': 'GER', 'team2': 'CUW', 't1': 'Germany', 't2': 'Curaçao', 'group': 'E', 'date': '2026-06-14 12:00', 'stadium': 'Houston Stadium', 'city': 'Houston'},
    {'team1': 'NED', 'team2': 'JPN', 't1': 'Netherlands', 't2': 'Japan', 'group': 'F', 'date': '2026-06-14 15:00', 'stadium': 'Dallas Stadium', 'city': 'Arlington'},
    {'team1': 'CIV', 'team2': 'ECU', 't1': 'Côte d\'Ivoire', 't2': 'Ecuador', 'group': 'E', 'date': '2026-06-14 18:00', 'stadium': 'Philadelphia Stadium', 'city': 'Philadelphia'},
    {'team1': 'SWE', 'team2': 'TUN', 't1': 'Sweden', 't2': 'Tunisia', 'group': 'F', 'date': '2026-06-14 21:00', 'stadium': 'Estadio Monterrey', 'city': 'Guadalupe'},

    # June 15
    {'team1': 'ESP', 'team2': 'CPV', 't1': 'Spain', 't2': 'Cape Verde', 'group': 'H', 'date': '2026-06-15 11:00', 'stadium': 'Atlanta Stadium', 'city': 'Atlanta'},
    {'team1': 'BEL', 'team2': 'EGY', 't1': 'Belgium', 't2': 'Egypt', 'group': 'G', 'date': '2026-06-15 14:00', 'stadium': 'Seattle Stadium', 'city': 'Seattle'},
    {'team1': 'SAU', 'team2': 'URU', 't1': 'Saudi Arabia', 't2': 'Uruguay', 'group': 'H', 'date': '2026-06-15 17:00', 'stadium': 'Miami Stadium', 'city': 'Miami Gardens'},
    {'team1': 'IRN', 'team2': 'NZL', 't1': 'Iran', 't2': 'New Zealand', 'group': 'G', 'date': '2026-06-15 20:00', 'stadium': 'Los Angeles Stadium', 'city': 'Inglewood'},

    # June 16
    {'team1': 'FRA', 'team2': 'SEN', 't1': 'France', 't2': 'Senegal', 'group': 'I', 'date': '2026-06-16 14:00', 'stadium': 'New York New Jersey Stadium', 'city': 'East Rutherford'},
    {'team1': 'IRQ', 'team2': 'NOR', 't1': 'Iraq', 't2': 'Norway', 'group': 'I', 'date': '2026-06-16 17:00', 'stadium': 'Boston Stadium', 'city': 'Foxborough'},
    {'team1': 'ARG', 'team2': 'ALG', 't1': 'Argentina', 't2': 'Algeria', 'group': 'J', 'date': '2026-06-16 20:00', 'stadium': 'Kansas City Stadium', 'city': 'Kansas City'},
    {'team1': 'AUT', 'team2': 'JOR', 't1': 'Austria', 't2': 'Jordan', 'group': 'J', 'date': '2026-06-16 23:00', 'stadium': 'San Francisco Bay Area Stadium', 'city': 'Santa Clara'},

    # June 17
    {'team1': 'POR', 'team2': 'COD', 't1': 'Portugal', 't2': 'DR Congo', 'group': 'K', 'date': '2026-06-17 12:00', 'stadium': 'Houston Stadium', 'city': 'Houston'},
    {'team1': 'ENG', 'team2': 'CRO', 't1': 'England', 't2': 'Croatia', 'group': 'L', 'date': '2026-06-17 15:00', 'stadium': 'Dallas Stadium', 'city': 'Arlington'},
    {'team1': 'GHA', 'team2': 'PAN', 't1': 'Ghana', 't2': 'Panama', 'group': 'L', 'date': '2026-06-17 18:00', 'stadium': 'Toronto Stadium', 'city': 'Toronto'},
    {'team1': 'UZB', 'team2': 'COL', 't1': 'Uzbekistan', 't2': 'Colombia', 'group': 'K', 'date': '2026-06-17 21:00', 'stadium': 'Mexico City Stadium', 'city': 'Mexico City'},
]

# Knockout stages placeholder schedule (dates in Central Time, mapped to brackets)
KNOCKOUT_MATCHES = [
    # Round of 16
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 49', 't2': 'Winner Match 50', 'group': '', 'stage': 'R16', 'date': '2026-07-04 12:00', 'stadium': 'SoFi Stadium', 'city': 'Los Angeles'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 51', 't2': 'Winner Match 52', 'group': '', 'stage': 'R16', 'date': '2026-07-04 16:00', 'stadium': 'MetLife Stadium', 'city': 'East Rutherford'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 53', 't2': 'Winner Match 54', 'group': '', 'stage': 'R16', 'date': '2026-07-05 12:00', 'stadium': 'BMO Field', 'city': 'Toronto'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 55', 't2': 'Winner Match 56', 'group': '', 'stage': 'R16', 'date': '2026-07-05 16:00', 'stadium': 'Mercedes-Benz Stadium', 'city': 'Atlanta'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 57', 't2': 'Winner Match 58', 'group': '', 'stage': 'R16', 'date': '2026-07-06 12:00', 'stadium': 'BC Place', 'city': 'Vancouver'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 59', 't2': 'Winner Match 60', 'group': '', 'stage': 'R16', 'date': '2026-07-06 16:00', 'stadium': 'Levi\'s Stadium', 'city': 'Santa Clara'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 61', 't2': 'Winner Match 62', 'group': '', 'stage': 'R16', 'date': '2026-07-07 12:00', 'stadium': 'Hard Rock Stadium', 'city': 'Miami'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner Match 63', 't2': 'Winner Match 64', 'group': '', 'stage': 'R16', 'date': '2026-07-07 16:00', 'stadium': 'Lumen Field', 'city': 'Seattle'},

    # Quarterfinals
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner R16-1', 't2': 'Winner R16-2', 'group': '', 'stage': 'QF', 'date': '2026-07-09 15:00', 'stadium': 'Gillette Stadium', 'city': 'Foxborough'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner R16-3', 't2': 'Winner R16-4', 'group': '', 'stage': 'QF', 'date': '2026-07-10 15:00', 'stadium': 'SoFi Stadium', 'city': 'Los Angeles'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner R16-5', 't2': 'Winner R16-6', 'group': '', 'stage': 'QF', 'date': '2026-07-11 12:00', 'stadium': 'Arrowhead Stadium', 'city': 'Kansas City'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner R16-7', 't2': 'Winner R16-8', 'group': '', 'stage': 'QF', 'date': '2026-07-11 16:00', 'stadium': 'Hard Rock Stadium', 'city': 'Miami'},

    # Semifinals
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner QF-1', 't2': 'Winner QF-2', 'group': '', 'stage': 'SF', 'date': '2026-07-14 15:00', 'stadium': 'AT&T Stadium', 'city': 'Arlington'},
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner QF-3', 't2': 'Winner QF-4', 'group': '', 'stage': 'SF', 'date': '2026-07-15 15:00', 'stadium': 'Mercedes-Benz Stadium', 'city': 'Atlanta'},

    # Third Place
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Loser SF-1', 't2': 'Loser SF-2', 'group': '', 'stage': 'THIRD', 'date': '2026-07-18 15:00', 'stadium': 'Hard Rock Stadium', 'city': 'Miami'},

    # Final
    {'team1': 'TBD', 'team2': 'TBD', 't1': 'Winner SF-1', 't2': 'Winner SF-2', 'group': '', 'stage': 'FINAL', 'date': '2026-07-19 15:00', 'stadium': 'MetLife Stadium', 'city': 'East Rutherford'},
]

class Command(BaseCommand):
    help = 'Seeds the database with exact FIFA World Cup 2026 match schedule'

    def handle(self, *args, **options):
        # Clear existing match data
        self.stdout.write('Clearing all existing matches...')
        Match.objects.all().delete()

        all_matches = GROUP_MATCHES + KNOCKOUT_MATCHES
        created = 0

        for i, m in enumerate(all_matches):
            dt_str = m['date']
            # Parse naïve time
            dt_naive = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            # Localize to US Central Time (CT)
            dt_ct = CT.localize(dt_naive)
            # Convert to Bangladesh Standard Time (BST)
            dt_bst = dt_ct.astimezone(BST)

            obj, was_created = Match.objects.get_or_create(
                team1_code=m['team1'],
                team2_code=m['team2'],
                group=m['group'],
                stage=m.get('stage', 'GROUP'),
                date_bst=dt_bst,
                defaults={
                    'team1_name': m['t1'],
                    'team2_name': m['t2'],
                    'stadium': m.get('stadium', ''),
                    'city': m.get('city', ''),
                    'status': 'UPCOMING',
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Seeded {created} matches (converted from CT to BST successfully).'))
