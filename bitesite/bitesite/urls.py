from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include

from bitesite import settings
from shortener.views import page_not_found, IndexHome, url_redirect

urlpatterns = [
    path('-/admin/', admin.site.urls),
    path('', IndexHome.as_view(), name='home'),
    path('-/', include('shortener.urls')),
    path('u/<str:slugs>/', url_redirect, kwargs={'is_free': True}),
    re_path('(?P<slugs>.+?)/', url_redirect, name='redirect'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = page_not_found
