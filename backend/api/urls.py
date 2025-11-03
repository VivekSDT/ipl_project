from django.urls import path
from . import views

urlpatterns = [
    path('matches-per-year/', views.matches_per_year, name='matches_per_year'),
    path('stacked-wins/', views.stacked_wins_per_team_per_year, name='stacked_wins'),
    path('extra-runs/<int:year>/', views.extra_runs_per_team, name='extra_runs'),
    path('top-economy/<int:year>/', views.top_economical_bowlers, name='top_economy'),
    path('matches-vs-wins/<int:year>/', views.matches_played_vs_won, name='matches_vs_wins'),
]
