from .views import *
from django.urls import path


urlpatterns = [
    path('Login/',LoginView.as_view(),name='Login'),
    path('Logout/',LogoutView.as_view(),name='Logout'),
]