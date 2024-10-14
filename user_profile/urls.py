from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_profile, name='user_profile'),
    path("update/", views.update_profile, name='update_profile'),
]
