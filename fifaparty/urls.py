from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('venues/', include('venues.urls')),
    path('schedule/', include('matches.urls')),
    path('notifications/', include('notifications.urls')),
    path('predictions/', include('predictions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
