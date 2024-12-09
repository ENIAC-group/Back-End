from django.urls import path 
from .views import *

urlpatterns = [
    path( 'MBTI/' , GetMBTItest.as_view({'post' : 'create' , 'get' : 'retrieve'}) , name='MBTI') ,
    path('glasser/' , GlasserTestView.as_view({'post' : 'create' , 'get' : 'retrieve'}) , name='glasser') ,
    path('tests/' , ThrepayTestsView.as_view({"get" : "get"}) , name="patient_tests")
]