# workpro/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(('intro.urls', 'intro'), namespace='intro')),
]

# Serve media files in both development and production (Railway ephemeral filesystem)
# For permanent storage, migrate to S3/Cloudinary in the future
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)