from django.urls import path
from . import views
from crud_operations_for_vehicles import views as crud_views

urlpatterns = [
    path('', views.vehicle_list, name='vehicle_list'),  # This serves as the home view
    path('home/', views.vehicle_list, name='home'),  # 'home' alias, but same view
    path('vehicle/<int:vehicle_id>/', views.vehicle_list, name='vehicle_detail'),  # Details view
    path('logout/', views.logout_view, name='logout'),

]
