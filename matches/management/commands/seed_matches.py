"""
Management command to seed FIFA World Cup 2026 group stage match data.
Run: python manage.py seed_matches
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, timedelta
from matches.models import Match
import pytz

BST = pytz.timezone('Asia/Dhaka')

# FIFA World Cup 2026 — Group Stage (sample data, real schedule TBD)
MATCHES = [
    # Group A
    {'team1': 'USA', 'team2': 'MEX', 't1': 'United States', 't2': 'Mexico', 'group': 'A', 'date': '2026-06-11 23:00', 'stadium': 'MetLife Stadium', 'city': 'New Jersey'},
    {'team1': 'CAN', 'team2': 'MAR', 't1': 'Canada', 't2': 'Morocco', 'group': 'A', 'date': '2026-06-12 05:00', 'stadium': 'SoFi Stadium', 'city': 'Los Angeles'},
    {'team1': 'MEX', 'team2': 'CAN', 't1': 'Mexico', 't2': 'Canada', 'group': 'A', 'date': '2026-06-15 23:00', 'stadium': 'AT&T Stadium', 'city': 'Dallas'},
    {'team1': 'USA', 'team2': 'MAR', 't1': 'United States', 't2': 'Morocco', 'group': 'A', 'date': '2026-06-16 02:00', 'stadium': 'Rose Bowl', 'city': 'Los Angeles'},
    # Group B
    {'team1': 'ARG', 'team2': 'ESP', 't1': 'Argentina', 't2': 'Spain', 'group': 'B', 'date': '2026-06-13 02:00', 'stadium': 'Hard Rock Stadium', 'city': 'Miami'},
    {'team1': 'BRA', 'team2': 'POR', 't1': 'Brazil', 't2': 'Portugal', 'group': 'B', 'date': '2026-06-13 23:00', 'stadium': 'Allegiant Stadium', 'city': 'Las Vegas'},
    {'team1': 'ARG', 'team2': 'BRA', 't1': 'Argentina', 't2': 'Brazil', 'group': 'B', 'date': '2026-06-17 02:00', 'stadium': 'MetLife Stadium', 'city': 'New Jersey'},
    {'team1': 'ESP', 'team2': 'POR', 't1': 'Spain', 't2': 'Portugal', 'group': 'B', 'date': '2026-06-17 23:00', 'stadium': 'Gillette Stadium', 'city': 'Boston'},
    # Group C
    {'team1': 'FRA', 'team2': 'GER', 't1': 'France', 't2': 'Germany', 'group': 'C', 'date': '2026-06-14 02:00', 'stadium': 'Empower Field', 'city': 'Denver'},
    {'team1': 'ENG', 'team2': 'NED', 't1': 'England', 't2': 'Netherlands', 'group': 'C', 'date': '2026-06-14 23:00', 'stadium': 'Levi\'s Stadium', 'city': 'San Francisco'},
    {'team1': 'FRA', 'team2': 'ENG', 't1': 'France', 't2': 'England', 'group': 'C', 'date': '2026-06-18 02:00', 'stadium': 'Lincoln Financial', 'city': 'Philadelphia'},
    {'team1': 'GER', 'team2': 'NED', 't1': 'Germany', 't2': 'Netherlands', 'group': 'C', 'date': '2026-06-18 23:00', 'stadium': 'MetLife Stadium', 'city': 'New Jersey'},
    # Group D
    {'team1': 'BEL', 'team2': 'JPN', 't1': 'Belgium', 't2': 'Japan', 'group': 'D', 'date': '2026-06-15 02:00', 'stadium': 'AT&T Stadium', 'city': 'Dallas'},
    {'team1': 'KOR', 'team2': 'AUS', 't1': 'South Korea', 't2': 'Australia', 'group': 'D', 'date': '2026-06-15 23:00', 'stadium': 'SoFi Stadium', 'city': 'Los Angeles'},
    {'team1': 'BEL', 'team2': 'KOR', 't1': 'Belgium', 't2': 'South Korea', 'group': 'D', 'date': '2026-06-19 02:00', 'stadium': 'Rose Bowl', 'city': 'Los Angeles'},
    {'team1': 'JPN', 'team2': 'AUS', 't1': 'Japan', 't2': 'Australia', 'group': 'D', 'date': '2026-06-19 23:00', 'stadium': 'Empower Field', 'city': 'Denver'},
]


class Command(BaseCommand):
    help = 'Seeds the database with FIFA World Cup 2026 match data'

    def handle(self, *args, **options):
        created = 0
        for i, m in enumerate(MATCHES):
            dt_str = m['date']
            dt_naive = datetime.strptime(dt_str, '%Y-%m-%d %H:%M')
            dt_bst = BST.localize(dt_naive)

            obj, was_created = Match.objects.get_or_create(
                team1_code=m['team1'],
                team2_code=m['team2'],
                group=m['group'],
                defaults={
                    'team1_name': m['t1'],
                    'team2_name': m['t2'],
                    'stage': 'GROUP',
                    'date_bst': dt_bst,
                    'stadium': m.get('stadium', ''),
                    'city': m.get('city', ''),
                    'status': 'UPCOMING',
                }
            )
            if was_created:
                created += 1

        self.stdout.write(self.style.SUCCESS(f'✅ Seeded {created} matches ({len(MATCHES) - created} already existed).'))
