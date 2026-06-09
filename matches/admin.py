from django.contrib import admin
from .models import Match


@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ['team1_name', 'team2_name', 'group', 'stage', 'date_bst', 'status', 'team1_score', 'team2_score']
    list_filter = ['stage', 'status', 'group']
    search_fields = ['team1_name', 'team2_name']
    ordering = ['date_bst']
    list_editable = ['status', 'team1_score', 'team2_score']
