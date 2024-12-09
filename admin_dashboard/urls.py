from django.urls import path
from .views import vehicle_list_view, dashboard_view, booking_list_view, users_view

urlpatterns = [
    path('', vehicle_list_view, name='vehicle_list'),
    path('bookings/', booking_list_view, name='bookings'),
    path('vehicles/', vehicle_list_view, name='vehicle_list'),
    path('users/', users_view, name='users'),
]
