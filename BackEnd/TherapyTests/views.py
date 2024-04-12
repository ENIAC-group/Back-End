from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.therapy_tests import GetMBTIresults
from counseling.models import Pationt 
from .models import TherapyTests
from rest_framework import status 
import json 
from django.http.request import QueryDict

class GetMBTItest(viewsets.ModelViewSet) : 
    permission_classes = [IsAuthenticated ]

    def create(self, request, *args, **kwargs):
        udata = request.data
        
        data = {}
        for key in udata.keys() : 
            data[int(key)] = udata[key]
        
        user = request.user
        pationt = Pationt.objects.filter(user = user).first()
        mbti = GetMBTIresults( data , user.gender )
        print(mbti)
        old_test = TherapyTests.objects.filter( pationt = pationt ).first()
        if old_test : 
            old_test.MBTItest = mbti['final']
            old_test.save()
            return Response( {'message' : 'test`s results was successfullly updated'} , status=status.HTTP_200_OK )
        else : 
            test = TherapyTests.objects.create( 
                pationt = pationt ,
                MBTItest = mbti['final']
            )
            return Response( {'message' : 'test`s results was successfullly registered'} , status=status.HTTP_200_OK )
    

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pationt = Pationt.objects.filter(user = user ).first()
        print(pationt)
        # mbti = pationt.therapytests 
        mbti = TherapyTests.objects.filter( pationt = pationt ).first()
        return Response( {"type" : mbti.MBTItest} , status=status.HTTP_200_OK )

