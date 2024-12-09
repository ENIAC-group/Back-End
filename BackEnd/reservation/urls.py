from django.urls import path
from .views import *

urlpatterns = [
    path("create/" , ReservationView.as_view({'post':'create'}) , name="create") , 
    path("delete/<int:pk>/" , ReservationView.as_view({'delete': 'destroy'}) , name="delete") , 
    path("between_dates/", ReservationView.as_view({'get': 'between_dates'}), name="between_dates"),
    path("last_month/" ,ReservationView.as_view({'get' : 'list_month'}),name="last_month" ),
    path("last_week/" , ReservationView.as_view({'get' : 'last_week'}) , name="last_week")
]
