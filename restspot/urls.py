from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('homepage.urls')),
    path('places/', include('places.urls')),
    path('visits/', include('visits.urls')),
    path('admin/', admin.site.urls),
]
