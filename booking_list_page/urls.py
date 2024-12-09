from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_list, name="booking_list"),
    path('rental-detail/<int:rental_id>/', views.rental_detail_view, name='rental_detail'),
]
