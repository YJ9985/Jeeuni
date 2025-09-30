from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('', RedirectView.as_view(url='/accounts/', permanent=False)),
    path('api/v1/', include('books.urls')),
    path('api/v2/', include('literacy.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)