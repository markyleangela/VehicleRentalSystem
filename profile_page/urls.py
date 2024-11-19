from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_profile, name='profile_page'),
    # path("update-profile/", views.update_profile, name='update_profile'),
    path('update-details/', views.update_details, name='update_details'),
  
    path('account-info/', views.change_password, name='account_info'),
    path('verify-profile/', views.license_verification_view, name='license_verification'),
]
