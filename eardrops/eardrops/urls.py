from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static

from eardrops.settings import STATIC_URL


urlpatterns = [
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
