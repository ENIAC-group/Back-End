from django.urls import path
from .views import *

urlpatterns = [
    path("get_rating/" , DoctorPanelView.as_view({'post':'get_rating'}) , name="GetRating") , 
    path("ThisWeekResevations/" , DoctorPanelView.as_view({'post':'ThisWeekResevations'}) , name="ReservationList") , 
    path("NextWeekReservations/" , DoctorPanelView.as_view({'post':'NextWeekReservations'}) , name="ReservationList2") , 


]
