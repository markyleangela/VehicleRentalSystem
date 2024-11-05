from django.urls import path
from . import views

urlpatterns = [
    path("<int:vehicle_id>/", views.booking_process, name="booking_process"),
    path("payment/<int:rental_id>/", views.payment, name="payment"),
    path("confirmation/<int:rental_id>/", views.booking_confirmation, name="booking_confirmation"),
]
