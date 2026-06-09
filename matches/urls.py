from django.urls import path
from . import views

urlpatterns = [
    path('', views.schedule, name='schedule'),
    path('<int:match_id>/', views.match_detail, name='match_detail'),
    path('api/live/', views.live_scores, name='live_scores'),
]
