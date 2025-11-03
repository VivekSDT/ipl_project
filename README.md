This repository contains a codebase
for the IPL analytics using dataset:(https://www.kaggle.com/manasgarg/ipl) (Django backend + Postgres + React frontend).

**What is included**
- backend/: Django project `ipl_django` and app `api` (models, views, management command to load CSVs)
- frontend/: React app skeleton using Material-UI and react-google-charts
- scripts to load the `matches.csv` and `deliveries.csv`

**How to use (quick)**
1. Install Postgres locally and clone the repo using :
   ```bash
   git clone https://github.com/VivekSDT/ipl_project.git
   ```
2. Create a Python virtualenv and install requirements from `backend/requirements.txt`.
3. Update `backend/ipl_django/settings_local.py` with your DB credentials.
4. Run migrations and then run the management command to load CSVs:
   ```bash
   python manage.py migrate
   python manage.py makemigrations
   python manage.py migrate
   python manage.py load_ipl_data --matches /path/to/matches.csv --deliveries /path/to/deliveries.csv
   ```
5. Start Django: `python manage.py runserver`
6. Frontend: `cd frontend && npm install && npm start` (proxy to backend configured)

See `backend/README.md` and `frontend/README.md` for detailed steps.
