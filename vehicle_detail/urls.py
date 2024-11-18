from django.urls import path
from . import views

urlpatterns = [
     path('vehicle/<int:vehicle_id>/', views.vehicle_detail, name='vehicle_detail'),
]
