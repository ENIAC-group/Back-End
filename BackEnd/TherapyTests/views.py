from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from utils.therapy_tests import GetMBTIresults ,GlasserResults
from counseling.models import Pationt 
from .models import TherapyTests , GlasserTest , MedicalRecord , TreatementHistory
from rest_framework import status 
import json 
from django.http.request import QueryDict
from .serializer import MedicalRecordSerializer
from django.forms.models import model_to_dict
# https://www.youtube.com/watch?v=P2_j1P51dNI&list=RD1mZhwXMl8vc&index=27

class MedicalRecordView(viewsets.ModelViewSet ) : 
    permission_classes = [IsAuthenticated]
    queryset = MedicalRecord.objects.all()
    http_method_names = ['get','post','retrieve','put','patch' , 'delete']
    serializer_class = MedicalRecordSerializer
    def create(self , request ) : 
        user = request.user 
        pationt = Pationt.objects.filter(user = user ).first()
        serializer = self.serializer_class(data= request.data )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.stored_validated_data 
        treatementHistory1 = None 
        treatementHistory2 = None 
        treatementHistory3 = None 
        if 'treatementHistory1' in validated_data.keys() : 
            treatementHistory1 = validated_data.get('treatementHistory1')
            tr1 = TreatementHistory.objects.create(
                end_date = treatementHistory1['end_date'] , 
                length = treatementHistory1['length'], 
                is_finished = treatementHistory1['is_finished'] , 
                reason_to_leave = treatementHistory1['reason_to_leave'] , 
                approach = treatementHistory1['approach'], 
                special_drugs = treatementHistory1['special_drugs']
            )
            treatementHistory1 = tr1
        if 'treatementHistory2' in validated_data.keys() : 
            treatementHistory2 = validated_data.get('treatementHistory2')
            tr2 = TreatementHistory.objects.create(
                end_date = treatementHistory2['end_date'] , 
                length = treatementHistory2['length'] , 
                is_finished = treatementHistory2['is_finished'], 
                reason_to_leave = treatementHistory2['reason_to_leave'], 
                approach = treatementHistory2['approach'], 
                special_drugs = treatementHistory2['special_drugs']
            )
            treatementHistory2 = tr2

        if 'treatementHistory3' in validated_data.keys() : 
            treatementHistory3 = validated_data.get("treatementHistory3")
            tr3 = TreatementHistory.objects.create(
                end_date = treatementHistory3['end_date'], 
                length = treatementHistory3['length'] , 
                is_finished = treatementHistory3['is_finished'], 
                reason_to_leave = treatementHistory3['reason_to_leave'], 
                approach = treatementHistory3['approach'], 
                special_drugs = treatementHistory3['special_drugs']
            )
            treatementHistory3 = tr3

        medical_record = MedicalRecord.objects.create(
            pationt = pationt , 
            child_num = validated_data.get('child_num') , 
            family_history= validated_data.get('family_history')  , 
            nationalID = validated_data.get('nationalID') , 
            treatementHistory1 = treatementHistory1 , 
            treatementHistory2 = treatementHistory2 , 
            treatementHistory3 = treatementHistory3
        )
     
        oi_dict = model_to_dict(medical_record)
        oi_serialized = json.dumps(oi_dict)
        data = {
            "medical_record" : oi_serialized , 
            "message" : "record has been successfully created."
        }
        return Response(data , status=status.HTTP_201_CREATED)
    

    def update(self , request ) : 
        user = request.user 
        pationt = Pationt.objects.filter(user = user ).first()
        serializer = self.serializer_class(data= request.data )
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.stored_validated_data 
        treatementHistory1 = None 
        treatementHistory2 = None 
        treatementHistory3 = None 
        old_record = MedicalRecord.objects.filter(pationt = pationt )

        if not old_record.exists() : 
            return Response({"message" : "this patient has not create a record yet."} , status=status.HTTP_400_BAD_REQUEST )
        
        old_record = old_record.first()

        if 'treatementHistory1' in validated_data.keys() : 
            treatementHistory1 = validated_data.get('treatementHistory1')
            if not old_record.treatementHistory1 : 
                tr1 = TreatementHistory.objects.create(
                    end_date = treatementHistory1['end_date'] , 
                    length = treatementHistory1['length'], 
                    is_finished = treatementHistory1['is_finished'] , 
                    reason_to_leave = treatementHistory1['reason_to_leave'] , 
                    approach = treatementHistory1['approach'], 
                    special_drugs = treatementHistory1['special_drugs']
                )
                old_record.treatementHistory1 = tr1
            else : 
                old_record.treatementHistory1.end_date = treatementHistory1['end_date'] 
                old_record.treatementHistory1.length = treatementHistory1['length']
                old_record.treatementHistory1.is_finished = treatementHistory1['is_finished'] 
                old_record.treatementHistory1.reason_to_leave = treatementHistory1['reason_to_leave'] 
                old_record.treatementHistory1.approach = treatementHistory1['approach']
                old_record.treatementHistory1.special_drugs = treatementHistory1['special_drugs']
            #     tr1 = old_record.treatementHistory1
            # treatementHistory1 = tr1
            old_record.treatementHistory1.save()

        if 'treatementHistory2' in validated_data.keys() : 
            treatementHistory2 = validated_data.get('treatementHistory2')
            if not old_record.treatementHistory2 : 
                tr2 = TreatementHistory.objects.create(
                    end_date = treatementHistory2['end_date'] , 
                    length = treatementHistory2['length'], 
                    is_finished = treatementHistory2['is_finished'] , 
                    reason_to_leave = treatementHistory2['reason_to_leave'] , 
                    approach = treatementHistory2['approach'], 
                    special_drugs = treatementHistory2['special_drugs']
                )
                old_record.treatementHistory2 = tr2 
            else : 
                old_record.treatementHistory2.end_date = treatementHistory2['end_date']
                old_record.treatementHistory2.length = treatementHistory2['length']
                old_record.treatementHistory2.is_finished = treatementHistory2['is_finished'] 
                old_record.treatementHistory2.reason_to_leave = treatementHistory2['reason_to_leave'] 
                old_record.treatementHistory2.approach = treatementHistory2['approach']
                old_record.treatementHistory2.special_drugs = treatementHistory2['special_drugs']
            #     tr2 = old_record.treatementHistory2

            old_record.treatementHistory2.save()
            # treatementHistory2 = tr2

        if 'treatementHistory3' in validated_data.keys() : 
            treatementHistory3 = validated_data.get('treatementHistory3')
            if not old_record.treatementHistory3 : 
                tr3 = TreatementHistory.objects.create(
                    end_date = treatementHistory2['end_date'] , 
                    length = treatementHistory2['length'], 
                    is_finished = treatementHistory2['is_finished'] , 
                    reason_to_leave = treatementHistory2['reason_to_leave'] , 
                    approach = treatementHistory2['approach'], 
                    special_drugs = treatementHistory2['special_drugs']
                )
                old_record.treatementHistory3 = tr3 
            else : 
                old_record.treatementHistory3.end_date = treatementHistory3['end_date'] 
                old_record.treatementHistory3.length = treatementHistory3['length']
                old_record.treatementHistory3.is_finished = treatementHistory3['is_finished']
                old_record.treatementHistory3.reason_to_leave = treatementHistory3['reason_to_leave'] 
                old_record.treatementHistory3.approach = treatementHistory3['approach']
                old_record.treatementHistory3.special_drugs = treatementHistory3['special_drugs']
            old_record.treatementHistory3.save()

        old_record.pationt = pationt 
        old_record.child_num = validated_data.get('child_num') 
        old_record.family_history= validated_data.get('family_history')  
        old_record.nationalID = validated_data.get('nationalID') 
        old_record.save()
        
        oi_dict = model_to_dict(old_record)
        oi_serialized = json.dumps(oi_dict)
        data = {
            "medical_record" : oi_serialized , 
            "message" : "record has been successfully updated."
        }

        return Response(data , status=status.HTTP_200_OK )
    

    
    def retrieve(self , request ) : 
        user = request.user 
        pationt = Pationt.objects.filter(user = user).first()
        record = self.queryset.filter( pationt = pationt )
        if not record.exists() : 
            return Response({"message" : "there is no any records with provided id."} , status=status.HTTP_400_BAD_REQUEST )
        oi = record.first() 
        oi_dict = model_to_dict(oi)
        
        if "treatementHistory3" in oi_dict :
            id = oi_dict["treatementHistory3"] 
            tre = TreatementHistory.objects.filter( id = id ).first()
            if tre : 
                oi_dict["treatementHistory3"] = model_to_dict(tre)
    
        if "treatementHistory1" in oi_dict :
            id = oi_dict["treatementHistory1"] 
            tre = TreatementHistory.objects.filter( id = id ).first()
            if tre : 
                oi_dict["treatementHistory1"] = model_to_dict(tre)

        if "treatementHistory2" in oi_dict :
            id = oi_dict["treatementHistory2"] 
            tre = TreatementHistory.objects.filter( id = id ).first()
            if tre : 
                oi_dict["treatementHistory2"] = model_to_dict(tre)

        # oi_serialized = json.dumps(oi_dict)
        data= {
            "record" : oi_dict
        }
       
        return Response(data= data , status=status.HTTP_200_OK )
    
    
    def delete(self , request ,id ) : 
        user = request.user 
        pationt = Pationt.objects.filter(user =user  ).first()
        if not pationt : 
            return Response({"message" : "there is no any records with provided id."} , status=status.HTTP_400_BAD_REQUEST )
        record = self.queryset.filter( id = id ).first()
        if not record : 
            return Response({"message" : "there is no any records with provided id."} , status=status.HTTP_400_BAD_REQUEST )
        record.delete()
        return Response({"message" : "record deleted successfully"} , status=status.HTTP_204_NO_CONTENT )


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


class GlasserTestView(viewsets.ModelViewSet) : 
    permission_classes = [IsAuthenticated]
    def create( self, request , *args , **kwargs ) : 
        req_data = {}
        d =  request.data["data"] 
        user = request.user
        data = json.loads(d)
        for key in data.keys() : 
            req_data[key] = data[key]
            data[key]
        if not req_data : 
            return Response({"message" : "test's results could not be empty!!!"} , status=status.HTTP_400_BAD_REQUEST)
        categories = GlasserResults( data=req_data )
        user = request.user
        pationt = Pationt.objects.filter(user = user).first()
        old_test = TherapyTests.objects.filter( pationt = pationt ).first()

        if not old_test : 
            old_test = TherapyTests.objects.create( pationt =pationt )
        
        if not old_test.glasserTest : 
            glasser = GlasserTest.objects.create(
                love = categories["love"] , 
                survive = categories["survive"] , 
                freedom = categories["freedom"] , 
                power = categories["power"] , 
                fun = categories["fun"]
            )
            old_test.glasserTest = glasser
            old_test.save()
            return Response( {'message' : 'test`s results was successfullly registerd'} , status=status.HTTP_200_OK ) 
        else :  
                glasser = old_test.glasserTest 
                glasser.love = categories["love"] , 
                glasser.survive = categories["survive"] , 
                glasser.freedom = categories["freedom"] , 
                glasser.power = categories["power"] , 
                glasser.fun = categories["fun"]
                glasser.save()    
                return Response( {'message' : 'test`s results was successfullly registered'} , status=status.HTTP_200_OK ) 
               

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
        mbti = TherapyTests.objects.filter( pationt = pationt ).first()
        return Response( {"type" : mbti.MBTItest} , status=status.HTTP_200_OK )

