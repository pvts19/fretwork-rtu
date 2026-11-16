from django.urls import path

from places import views

app_name = 'places'

urlpatterns = [
    path('', views.place_list, name='list'),
    path('free/', views.free_places, name='free'),
    path('create/', views.place_create, name='create'),
    path('<slug:slug>/', views.place_detail, name='detail'),
    path('<slug:slug>/edit/', views.place_edit, name='edit'),
]
