import requests
import pytz
from datetime import datetime
from django.utils import timezone
from matches.models import Match

def sync_matches_from_api():
    """
    Fetches real-time match data, teams, and stadiums from the public FIFA 2026 API,
    converts kickoff times to BST (UTC+6) correctly, and saves them to the database.
    Fails gracefully to preserve existing local data in case of API offline/network issues.
    """
    try:
        # 1. Fetch qualified teams list
        teams_resp = requests.get('https://worldcup26.ir/get/teams', timeout=5)
        if teams_resp.status_code != 200:
            raise ValueError(f"Teams API returned status code {teams_resp.status_code}")
        teams_data = teams_resp.json()
        teams_map = {t['id']: t for t in teams_data.get('teams', [])}

        # 2. Fetch stadiums list
        stadiums_resp = requests.get('https://worldcup26.ir/get/stadiums', timeout=5)
        if stadiums_resp.status_code != 200:
            raise ValueError(f"Stadiums API returned status code {stadiums_resp.status_code}")
        stadiums_data = stadiums_resp.json()
        stadiums_map = {s['id']: s for s in stadiums_data.get('stadiums', [])}

        # 3. Fetch matches list
        games_resp = requests.get('https://worldcup26.ir/get/games', timeout=5)
        if games_resp.status_code != 200:
            raise ValueError(f"Games API returned status code {games_resp.status_code}")
        games_data = games_resp.json()

        # Timezones mappings (region field in API -> local tz)
        tz_regions = {
            'Western': pytz.timezone('America/Los_Angeles'),
            'Central': pytz.timezone('America/Chicago'),
            'Eastern': pytz.timezone('America/New_York'),
        }
        bst = pytz.timezone('Asia/Dhaka')

        # Map API type string to Match stage model code
        stage_map = {
            'group': 'GROUP',
            'r32': 'R32',
            'r16': 'R16',
            'qf': 'QF',
            'sf': 'SF',
            'third': 'THIRD',
            'final': 'FINAL',
        }

        # Sync all matches
        for game in games_data.get('games', []):
            game_id = int(game['id'])

            # Determine home team properties
            home_id = game.get('home_team_id')
            home_team = teams_map.get(home_id, {})
            home_code = home_team.get('fifa_code', 'TBD')
            home_name = home_team.get('name_en', game.get('home_team_name_en', 'TBD'))

            # Determine away team properties
            away_id = game.get('away_team_id')
            away_team = teams_map.get(away_id, {})
            away_code = away_team.get('fifa_code', 'TBD')
            away_name = away_team.get('name_en', game.get('away_team_name_en', 'TBD'))

            # Handle placeholder knockout teams (label fields)
            if home_id == "0":
                home_code = 'TBD'
                home_name = game.get('home_team_label', 'TBD')
            if away_id == "0":
                away_code = 'TBD'
                away_name = game.get('away_team_label', 'TBD')

            # Map stadium & region timezone
            stadium_id = game.get('stadium_id')
            stadium_info = stadiums_map.get(stadium_id, {})
            stadium_name = stadium_info.get('fifa_name', stadium_info.get('name_en', ''))
            stadium_city = stadium_info.get('city_en', '')
            stadium_region = stadium_info.get('region', 'Central')

            # Parse and localize date/time
            local_date_str = game.get('local_date')
            try:
                # Format: MM/DD/YYYY HH:MM
                dt_naive = datetime.strptime(local_date_str, '%m/%d/%Y %H:%M')
                tz = tz_regions.get(stadium_region, tz_regions['Central'])
                dt_local = tz.localize(dt_naive)
                dt_bst = dt_local.astimezone(bst)
            except Exception:
                dt_bst = timezone.now()

            # Scores & Status updates
            home_score = int(game['home_score']) if game.get('home_score') is not None and game['home_score'] != 'null' else None
            away_score = int(game['away_score']) if game.get('away_score') is not None and game['away_score'] != 'null' else None

            finished = game.get('finished') == 'TRUE'
            time_elapsed = game.get('time_elapsed', 'notstarted')

            if finished:
                status = 'COMPLETED'
            elif time_elapsed != 'notstarted':
                status = 'LIVE'
            else:
                status = 'UPCOMING'

            # Save explicitly specifying ID to keep IDs completely aligned with the API (1 to 104)
            Match.objects.update_or_create(
                id=game_id,
                defaults={
                    'match_id': game_id,
                    'team1_code': home_code,
                    'team2_code': away_code,
                    'team1_name': home_name,
                    'team2_name': away_name,
                    'group': game.get('group', ''),
                    'stage': stage_map.get(game.get('type'), 'GROUP'),
                    'date_bst': dt_bst,
                    'stadium': stadium_name,
                    'city': stadium_city,
                    'status': status,
                    'team1_score': home_score,
                    'team2_score': away_score,
                }
            )
        print("Successfully synchronized all matches from the API.")
    except Exception as e:
        print(f"Silent warning: Could not synchronize matches from API: {e}. Preserved existing database values.")
