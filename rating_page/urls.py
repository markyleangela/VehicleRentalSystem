from django.urls import path
from . import views

urlpatterns = [
    path('', views.vehicle_rate, name='vehicle_rate'),
]
