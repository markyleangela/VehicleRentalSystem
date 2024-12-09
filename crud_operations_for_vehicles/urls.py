from django.urls import path
from . import views

urlpatterns = [
    path('create_vehicle/', views.create_vehicle_page, name='create_vehicle_page'),
    path('<int:vehicle_id>/update_vehicle/', views.update_vehicle_page, name='update_vehicle_page'),
    path('<int:vehicle_id>/', views.vehicle_detail, name='read_vehicle'),
]
