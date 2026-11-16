from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('places/', include('places.urls')),
    path('visits/', include('visits.urls')),
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'RestSpot — администрирование'
admin.site.site_title = 'RestSpot'
admin.site.index_title = 'Управление данными'

if 'debug_toolbar' in settings.INSTALLED_APPS:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))
