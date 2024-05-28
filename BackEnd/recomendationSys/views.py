from django.shortcuts import render
from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import serializers 
from rest_framework import status 
from datetime import datetime , date , timedelta 
from django.utils import timezone
from django.http.request import QueryDict
from django.forms.models import model_to_dict

# https://www.youtube.com/watch?v=P2_j1P51dNI&list=RD1mZhwXMl8vc&index=27

class MedicalRecordView(viewsets.ModelViewSet ) : 
    permission_classes = [IsAuthenticated]
    