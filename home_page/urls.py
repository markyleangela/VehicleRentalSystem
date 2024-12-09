from django.urls import path
from . import views


urlpatterns = [
    path("", views.vehicle_list, name='home'),
    path('logout/', views.logout_view, name='logout'),
]
