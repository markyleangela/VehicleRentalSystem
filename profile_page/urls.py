from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_profile, name='profile_page'),
    path("update/", views.update_profile, name='update_profile'),
]
