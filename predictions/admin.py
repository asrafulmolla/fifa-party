from django.contrib import admin
from .models import Prediction, PollResponse


@admin.register(Prediction)
class PredictionAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'predicted_winner', 'is_correct', 'created_at']
    list_filter = ['is_correct']
    list_editable = ['is_correct']


@admin.register(PollResponse)
class PollResponseAdmin(admin.ModelAdmin):
    list_display = ['user', 'match', 'mood', 'created_at']
    list_filter = ['mood']
