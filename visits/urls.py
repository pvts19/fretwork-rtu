from django.urls import path

from visits import views

app_name = 'visits'

urlpatterns = [
    path('', views.visit_list, name='list'),
    path('stats/', views.stats, name='stats'),
    path('create/', views.visit_create, name='create'),
    path('<int:visit_id>/', views.visit_detail, name='detail'),
    path('<int:visit_id>/edit/', views.visit_edit, name='edit'),
    path('<int:visit_id>/cancel/', views.visit_cancel, name='cancel'),
]
