from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_vehicle_page, name='create_vehicle_page'),
    path('<int:vehicle_id>/update/', views.update_vehicle_page, name='update_vehicle_page'),
]
