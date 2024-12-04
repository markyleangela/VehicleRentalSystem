from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_profile, name='profile_page'),
    # path("update-profile/", views.update_profile, name='update_profile'),
    path('update-details/', views.update_details, name='update_details'),
  
    path('account-info/', views.change_password, name='account_info'),
    path('verify-license/', views.license_verification_view, name='license_verification'),
    # path('confirm/<str:confirmation_code>/', views.confirm_email, name='confirm_email'),
    path('confirm-email/', views.confirm_email, name='confirm_email'),
    path('confirm-license/', views.confirm_license, name='confirm_license'),
    path('verify-email/', views.email_verification_form, name='verify_email'),
    path('confirm_delete/', views.confirm_delete_account, name='confirm_delete_account'),
   
    
]
