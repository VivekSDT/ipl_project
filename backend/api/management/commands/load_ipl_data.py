"""Django management command: load_ipl_data

Usage:
  python manage.py load_ipl_data --matches /path/to/matches.csv --deliveries /path/to/deliveries.csv

This command reads the CSVs using pandas and bulk-creates Match and Delivery rows.
It clears existing data for a clean load. It uses transactions and bulk_create for speed.
"""
import pandas as pd
from django.core.management.base import BaseCommand
from django.db import transaction
from api.models import Match, Delivery

class Command(BaseCommand):
    help = 'Load matches.csv and deliveries.csv into the database.'

    def add_arguments(self, parser):
        parser.add_argument('--matches', type=str, required=True, help='Path to matches.csv')
        parser.add_argument('--deliveries', type=str, required=True, help='Path to deliveries.csv')

    def handle(self, *args, **options):
        matches_csv = options['matches']
        deliveries_csv = options['deliveries']

        self.stdout.write('Reading matches CSV...')
        matches_df = pd.read_csv(matches_csv)
        self.stdout.write(f'Found {len(matches_df)} matches rows.')

        self.stdout.write('Reading deliveries CSV... (this may take a while)')
        deliveries_df = pd.read_csv(deliveries_csv)
        self.stdout.write(f'Found {len(deliveries_df)} deliveries rows.')

        with transaction.atomic():
            self.stdout.write('Clearing existing data...')
            Delivery.objects.all().delete()
            Match.objects.all().delete()

            self.stdout.write('Creating Match objects...')
            match_objs = []
            for _, row in matches_df.iterrows():
                m = Match(
                    match_id = int(row['id']),
                    season = int(row['season']) if not pd.isna(row['season']) else None,
                    city = row.get('city') if not pd.isna(row.get('city')) else None,
                    date = pd.to_datetime(row.get('date')).date() if not pd.isna(row.get('date')) else None,
                    team1 = row.get('team1'),
                    team2 = row.get('team2'),
                    toss_winner = row.get('toss_winner'),
                    toss_decision = row.get('toss_decision'),
                    result = row.get('result'),
                    dl_applied = int(row.get('dl_applied') or 0),
                    winner = row.get('winner'),
                    win_by_runs = int(row.get('win_by_runs') or 0),
                    win_by_wickets = int(row.get('win_by_wickets') or 0),
                    player_of_match = row.get('player_of_match'),
                    venue = row.get('venue'),
                    umpire1 = row.get('umpire1') if not pd.isna(row.get('umpire1')) else None,
                    umpire2 = row.get('umpire2') if not pd.isna(row.get('umpire2')) else None,
                    umpire3 = row.get('umpire3') if not pd.isna(row.get('umpire3')) else None,
                )
                match_objs.append(m)
            Match.objects.bulk_create(match_objs, batch_size=500)
            self.stdout.write(f'Inserted {len(match_objs)} matches.')

            # Build a map of match_id -> Match instance for FK resolution
            match_map = {m.match_id: m for m in Match.objects.all()}

            self.stdout.write('Creating Delivery objects... (bulk inserts)')
            deliveries = []
            created = 0
            for _, r in deliveries_df.iterrows():
                mid = int(r['match_id'])
                match_obj = match_map.get(mid)
                if not match_obj:
                    continue
                d = Delivery(
                    match = match_obj,
                    inning = int(r['inning']) if not pd.isna(r['inning']) else 0,
                    batting_team = r.get('batting_team'),
                    bowling_team = r.get('bowling_team'),
                    over = int(r['over']) if not pd.isna(r['over']) else 0,
                    ball = int(r['ball']) if not pd.isna(r['ball']) else 0,
                    batsman = r.get('batsman'),
                    non_striker = r.get('non_striker'),
                    bowler = r.get('bowler'),
                    is_super_over = int(r.get('is_super_over') or 0),
                    wide_runs = int(r.get('wide_runs') or 0),
                    bye_runs = int(r.get('bye_runs') or 0),
                    legbye_runs = int(r.get('legbye_runs') or 0),
                    noball_runs = int(r.get('noball_runs') or 0),
                    penalty_runs = int(r.get('penalty_runs') or 0),
                    batsman_runs = int(r.get('batsman_runs') or 0),
                    extra_runs = int(r.get('extra_runs') or 0),
                    total_runs = int(r.get('total_runs') or 0),
                    player_dismissed = r.get('player_dismissed') if not pd.isna(r.get('player_dismissed')) else None,
                    dismissal_kind = r.get('dismissal_kind') if not pd.isna(r.get('dismissal_kind')) else None,
                    fielder = r.get('fielder') if not pd.isna(r.get('fielder')) else None,
                )
                deliveries.append(d)
                if len(deliveries) >= 4000:
                    Delivery.objects.bulk_create(deliveries, batch_size=2000)
                    created += len(deliveries)
                    deliveries = []
            if deliveries:
                Delivery.objects.bulk_create(deliveries, batch_size=2000)
                created += len(deliveries)
            self.stdout.write(f'Inserted {created} deliveries.')

        self.stdout.write('Load complete.')
