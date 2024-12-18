"""
URL configuration for vrs project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("landing_page.urls")),

    path('login/', include("login_page.urls")),
    path('register/', include("register.urls")),
    path('create_vehicle/', include("crud_operations_for_vehicles.urls")),
    path('profile/', include("profile_page.urls")),
    path('vehicles/', include("crud_operations_for_vehicles.urls")),
    path('home/', include("home_page.urls")),
    path('booking_list/', include("booking_list_page.urls")),

    path('booking/', include("booking_process_page.urls")),

    path('vehicle_rating/', include("rating_page.urls")),
    path('vehicle_view/', include("vehicle_detail.urls")),
    path('about_us/', include("about_us.urls")),
    path('contact_us/', include("contact_page.urls")),
    path('admin_booking/', include('booking_list_admin.urls')),
    path('dashboard/', include('admin_dashboard.urls')),


]
