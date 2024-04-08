from django.urls import path
from .views import *

urlpatterns = [
    path("create/" , ReservationView.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}) , name="create") , 
    path("delete/<int:pk>/" , ReservationView.as_view({'delete': 'destroy'}) , name="delete") , 
]