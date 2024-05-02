from django.urls import path
from .views import *

urlpatterns = [
    path("get_rating/" , DoctorPanelView.as_view({'post':'get_rating'}) , name="GetRating") , 

]
