from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Serve favicon from /static/ — browsers request these from the root
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico', permanent=True)),
    path('favicon.png', RedirectView.as_view(url='/static/favicon.png', permanent=True)),
    path('', include('core.urls')),
    path('', include('accounts.urls')),
    path('venues/', include('venues.urls')),
    path('schedule/', include('matches.urls')),
    path('notifications/', include('notifications.urls')),
    path('predictions/', include('predictions.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

