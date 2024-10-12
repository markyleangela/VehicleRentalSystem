from django.urls import path
from . import views

urlpatterns = [
        path('', views.create_vehicle_page, name='create_vehicle_page'),
]