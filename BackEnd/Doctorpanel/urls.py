from django.urls import path
from .views import *

urlpatterns = [
    path("get_rating/<int:psychiatrist_id>/" , DoctorPanelView.as_view({'get':'get_rating'}) , name="GetRating") , 
    path("ThisWeekResevations/<int:psychiatrist_id>/" , DoctorPanelView.as_view({'get':'ThisWeekResevations'}) , name="ReservationList") , 
    path("NextWeekReservations/<int:psychiatrist_id>/" , DoctorPanelView.as_view({'get':'NextWeekReservations'}) , name="ReservationList2") , 
    path('doctor/free-time/', DoctorPanelView.as_view({'post':'PostFreeTime'})),


]
