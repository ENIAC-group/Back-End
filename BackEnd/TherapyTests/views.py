from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.therapy_tests import GetMBTIresults ,GlasserResults
from counseling.models import Pationt 
from .models import TherapyTests , GlasserTest 
from rest_framework import status 
import json 
from django.http.request import QueryDict


class ThrepayTestsView(viewsets.ModelViewSet ) : 
    permission_classes = [IsAuthenticated]
    def get( self , request ) : 
        user = request.user
        pationt = Pationt.objects.filter(user = user ).first()
        if not pationt : 
            Response({"message" : "there is not patient"} , status=status.HTTP_400_BAD_REQUEST )
        test = TherapyTests.objects.filter( pationt = pationt ).first()
        if not test : 
            Response({"message" : "this user hasn't take any tests!"} , status=status.HTTP_400_BAD_REQUEST)
        
        return Response( {"TherapTests" : test} , status=status.HTTP_200_OK )


class GlasserTestView(viewsets.ModelViewSet ) : 
    permission_classes = [IsAuthenticated]
    def create( self, request , *args , **kwargs ) : 
        req_data = {}
        d =  request.data["data"] 
        data = json.loads(d)
        for key in data.keys() : 
            print(data[key])
            req_data[key] = data[key]
            data[key]
        print( req_data )
        if not req_data : 
            return Response({"message" : "test's results could not be empty!!!"} , status=status.HTTP_400_BAD_REQUEST)
        categories = GlasserResults( data=req_data )
        glasser = GlasserTest.objects.create(
            love = categories["love"] , 
            survive = categories["survive"] , 
            freedom = categories["freedom"] , 
            power = categories["power"] , 
            fun = categories["fun"]
        )
        user = request.user
        pationt = Pationt.objects.filter(user = user).first()
        old_test = TherapyTests.objects.filter( pationt = pationt ).first()
        if old_test : 
            old_test.glasserTest = glasser
            old_test.save()
            data = {
                'message' : 'test`s results was successfullly updated' ,   
                "result" :  categories
            }
            return Response( data = data , status=status.HTTP_200_OK )
        else : 
            test = TherapyTests.objects.create( 
                pationt = pationt ,
                glasserTest = glasser 
            )
            data = {
                'message' : 'test`s results was successfullly registered' ,   
                "result" : categories
            }
            return Response(data=data  , status=status.HTTP_200_OK ) 
               

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pationt = Pationt.objects.filter(user = user ).first()
        print(pationt)
        mbti = TherapyTests.objects.filter( pationt = pationt ).first()
        return Response( {"glasser" : mbti.glasserTest} , status=status.HTTP_200_OK )
            

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
        
        old_test = TherapyTests.objects.filter( pationt = pationt ).first()
        if old_test : 
            old_test.MBTItest = mbti['final']
            old_test.save()
            data = {
                'message' : 'test`s results was successfullly updated' , 
                "result" : mbti["final"] 
            }
            return Response( data= data , status=status.HTTP_200_OK )
        else : 
            test = TherapyTests.objects.create( 
                pationt = pationt ,
                MBTItest = mbti['final']
            )
            data = {
                'message' : 'test`s results was successfullly registered' , 
                "result" : mbti["final"] 
            }
            return Response( data= data , status=status.HTTP_200_OK )
    

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        pationt = Pationt.objects.filter(user = user ).first()
        print(pationt)
        # mbti = pationt.therapytests 
        mbti = TherapyTests.objects.filter( pationt = pationt ).first()
        return Response( {"type" : mbti.MBTItest} , status=status.HTTP_200_OK )

