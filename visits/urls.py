from django.urls import path

from visits import views

app_name = 'visits'

urlpatterns = [
    path('', views.visit_list, name='list'),
    path('stats/', views.stats, name='stats'),
    path('<int:visit_id>/', views.visit_detail, name='detail'),
]
