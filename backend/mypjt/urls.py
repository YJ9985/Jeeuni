from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from .views import api_root, api_v1_root, api_v2_root, health_check

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='/accounts/', permanent=False)),
    path('api/', api_root),
    path('api/v1/', api_v1_root),
    path('api/v2/', api_v2_root),
    path('api/v1/', include('books.urls')),
    path('api/v2/', include('literacy.urls')),
    path('api/health/', health_check),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
