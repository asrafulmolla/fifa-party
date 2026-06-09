from django.urls import path
from . import views

urlpatterns = [
    path('predict/<int:match_id>/', views.predict, name='predict'),
    path('poll/<int:match_id>/', views.mood_poll, name='mood_poll'),
    path('poll/<int:match_id>/results/', views.poll_results, name='poll_results'),
]
