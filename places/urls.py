from django.urls import path

from places import views

urlpatterns = [
    path('', views.place_list),
    path('<int:place_id>/', views.place_detail),
]
