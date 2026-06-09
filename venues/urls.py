from django.urls import path
from . import views

urlpatterns = [
    path('', views.venue_list, name='venue_list'),
    path('add/', views.add_venue, name='add_venue'),
    path('<int:venue_id>/', views.venue_detail, name='venue_detail'),
    path('checkin/', views.toggle_checkin, name='toggle_checkin'),
]
