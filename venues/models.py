from django.db import models
from django.contrib.auth.models import User
from matches.models import Match

ENTRY_CHOICES = [
    ('FREE', 'Free Entry'),
    ('PAID', 'Paid Entry'),
    ('DONATION', 'Donation'),
]

SCREEN_CHOICES = [
    ('TV', 'Small TV'),
    ('BIG', 'Big Screen'),
    ('PROJECTOR', 'Full Projector'),
]

CAPACITY_CHOICES = [
    ('SMALL', 'Small (< 20)'),
    ('MEDIUM', 'Medium (20–100)'),
    ('LARGE', 'Large (100+)'),
]


class WatchVenue(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    area = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    submitted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='venues')
    entry_type = models.CharField(max_length=10, choices=ENTRY_CHOICES, default='FREE')
    entry_fee_details = models.CharField(max_length=200, blank=True)
    screen_size = models.CharField(max_length=15, choices=SCREEN_CHOICES, default='BIG')
    crowd_capacity = models.CharField(max_length=10, choices=CAPACITY_CHOICES, default='MEDIUM')
    contact_info = models.CharField(max_length=300, blank=True)
    photo = models.ImageField(upload_to='venues/', null=True, blank=True)
    verified = models.BooleanField(default=False)
    community_rating = models.FloatField(default=0.0)
    rating_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def checkin_count(self):
        return sum(vm.checkin_set.count() for vm in self.venue_matches.all())

    def __str__(self):
        return f"{self.name} ({self.area})"


class VenueMatch(models.Model):
    venue = models.ForeignKey(WatchVenue, on_delete=models.CASCADE, related_name='venue_matches')
    match = models.ForeignKey(Match, on_delete=models.CASCADE, related_name='venue_matches')
    
    class Meta:
        unique_together = ['venue', 'match']

    def __str__(self):
        return f"{self.venue.name} – {self.match}"


class CheckIn(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkins')
    venue_match = models.ForeignKey(VenueMatch, on_delete=models.CASCADE, related_name='checkin_set')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'venue_match']

    def __str__(self):
        return f"{self.user.username} @ {self.venue_match}"


class VenueRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    venue = models.ForeignKey(WatchVenue, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(default=5)  # 1-5
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'venue']
