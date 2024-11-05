from django.urls import path
from . import views

urlpatterns = [
    path("<int:vehicle_id>/", views.booking_process, name="booking_process"),
]
