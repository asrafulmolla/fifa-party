from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'supported_team', 'fan_score', 'created_at']
    list_filter = ['supported_team']
    search_fields = ['user__username', 'user__email']
    ordering = ['-fan_score']
