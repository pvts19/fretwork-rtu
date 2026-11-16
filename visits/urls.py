from django.urls import path

from visits import views

urlpatterns = [
    path('', views.visit_list),
    path('<int:visit_id>/', views.visit_detail),
]
