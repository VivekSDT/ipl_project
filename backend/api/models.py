from django.db import models

class Match(models.Model):
    match_id = models.IntegerField(primary_key=True)
    season = models.IntegerField(db_index=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100, blank=True, null=True)
    toss_decision = models.CharField(max_length=10, blank=True, null=True)
    result = models.CharField(max_length=50, blank=True, null=True)
    dl_applied = models.IntegerField(blank=True, null=True)
    winner = models.CharField(max_length=100, blank=True, null=True)
    win_by_runs = models.IntegerField(blank=True, null=True)
    win_by_wickets = models.IntegerField(blank=True, null=True)
    player_of_match = models.CharField(max_length=100, blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True, null=True)
    umpire1 = models.CharField(max_length=100, blank=True, null=True)
    umpire2 = models.CharField(max_length=100, blank=True, null=True)
    umpire3 = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        db_table = 'matches'
        ordering = ['season', 'match_id']

    def __str__(self):
        return f"{self.season} - {self.team1} vs {self.team2}"

class Delivery(models.Model):
    id = models.BigAutoField(primary_key=True)
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='deliveries')
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=200, blank=True, null=True)
    non_striker = models.CharField(max_length=200, blank=True, null=True)
    bowler = models.CharField(max_length=200)
    is_super_over = models.IntegerField(blank=True, null=True)
    wide_runs = models.IntegerField(blank=True, null=True)
    bye_runs = models.IntegerField(blank=True, null=True)
    legbye_runs = models.IntegerField(blank=True, null=True)
    noball_runs = models.IntegerField(blank=True, null=True)
    penalty_runs = models.IntegerField(blank=True, null=True)
    batsman_runs = models.IntegerField(blank=True, null=True)
    extra_runs = models.IntegerField(blank=True, null=True)
    total_runs = models.IntegerField(blank=True, null=True)
    player_dismissed = models.CharField(max_length=200, blank=True, null=True)
    dismissal_kind = models.CharField(max_length=100, blank=True, null=True)
    fielder = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        db_table = 'deliveries'
        indexes = [
            models.Index(fields=['bowler']),
            models.Index(fields=['bowling_team']),
            models.Index(fields=['match']),
        ]

    def __str__(self):
        return f"{self.match_id} {self.over}.{self.ball} {self.batsman} vs {self.bowler}"
