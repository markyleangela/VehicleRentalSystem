from django.urls import path
from . import views

urlpatterns = [
    path('<int:rental_id>/rental_detail/', views.rental_details_view, name='rental_details_admin'),
]
