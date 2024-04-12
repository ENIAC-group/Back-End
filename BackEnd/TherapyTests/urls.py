from django.urls import path 
from .views import *

urlpatterns = [
    path( 'MBTI/' , GetMBTItest.as_view({'post' : 'create' , 'get' : 'retrieve'}) , name='MBTI') , 
]