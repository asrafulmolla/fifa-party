from django.db import models
from django.contrib.auth.models import User
from matches.models import Match, TEAM_CHOICES

MOOD_CHOICES = [
    ('AMAZING', 'Amazing'),
    ('DECENT', 'Decent'),
    ('DISAPPOINTING', 'Disappointing'),
]


class Prediction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='predictions')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='predictions')
    predicted_winner = models.CharField(max_length=10, choices=TEAM_CHOICES)
    is_correct = models.BooleanField(null=True, blank=True)  # null = not yet determined
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'match']

    def __str__(self):
        return f"{self.user.username} predicts {self.predicted_winner} for {self.match}"


class PollResponse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='poll_responses')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='poll_responses')
    mood = models.CharField(max_length=15, choices=MOOD_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'match']

    def __str__(self):
        return f"{self.user.username}: {self.match} – {self.mood}"
