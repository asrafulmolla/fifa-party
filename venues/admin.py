from django.contrib import admin
from .models import WatchVenue, VenueMatch, CheckIn, VenueRating


class VenueMatchInline(admin.TabularInline):
    model = VenueMatch
    extra = 1


@admin.register(WatchVenue)
class WatchVenueAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'submitted_by', 'entry_type', 'verified', 'created_at']
    list_filter = ['entry_type', 'verified', 'screen_size', 'crowd_capacity']
    search_fields = ['name', 'area', 'address']
    list_editable = ['verified']
    inlines = [VenueMatchInline]


@admin.register(CheckIn)
class CheckInAdmin(admin.ModelAdmin):
    list_display = ['user', 'venue_match', 'timestamp']
    list_filter = ['timestamp']
