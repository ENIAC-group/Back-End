from django.urls import path 
from .views import *

urlpatterns = [
    path( 'MBTI/' , GetMBTItest.as_view({'post' : 'create' , 'get' : 'retrieve'}) , name='MBTI') ,
    path('glasser/' , GlasserTestView.as_view({'post' : 'create' , 'get' : 'retrieve'}) , name='glasser') ,
    path('tests/' , ThrepayTestsView.as_view({"get" : "get"}) , name="patient_tests") , 
    # path('record/<int:id>/' , MedicalRecordView.as_view( {'get' : 'retrieve' , 'delete' : 'delete'}) , name='patient_record') , 
    path('record/' , MedicalRecordView.as_view({'post' : 'create' , 'put' : 'update' , 'get' : 'retrieve' , 'delete' : 'delete'}) , name='records_ops')
]