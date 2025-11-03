# Backend (Django + DRF) - IPL Analytics

This folder contains a straightforward Django project `ipl_django` and a single app `api`.
It uses PostgreSQL as requested.

## Quick start (local Postgres)
1. Create and activate a Python virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
2. Configure DB in `ipl_django/settings_local.py` (copy settings_local.example.py to settings_local.py)
3. Run initial migrations:
   ```bash
   python manage.py migrate
   ```
4. Run main app migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
5. Load CSVs (use the files you uploaded):
   ```bash
   python manage.py load_ipl_data --matches /full/path/to/matches.csv --deliveries /full/path/to/deliveries.csv
   ```
6. Run the server:
   ```bash
   python manage.py runserver
   ```

API endpoints (examples)
- GET /api/matches-per-year/
- GET /api/stacked-wins/
- GET /api/extra-runs/<year>/
- GET /api/top-economy/<year>/
- GET /api/matches-vs-wins/<year>/

