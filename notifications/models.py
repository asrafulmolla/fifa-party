from django.db import models
from django.contrib.auth.models import User

NOTIFICATION_TYPES = [
    ('MATCH_SOON', 'Match Starting Soon'),
    ('NEW_VENUE', 'New Venue Near You'),
    ('CHECKIN_MILESTONE', 'Check-in Milestone'),
    ('VENUE_VERIFIED', 'Venue Verified'),
    ('PREDICTION_RESULT', 'Prediction Result'),
    ('GENERAL', 'General'),
]


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=25, choices=NOTIFICATION_TYPES, default='GENERAL')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=300, blank=True)  # URL to redirect on click
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.notification_type}] {self.user.username}: {self.title}"
