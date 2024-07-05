from rest_framework import serializers
from accounts.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import password_validation
from django.core import exceptions as exception
from .models import Reservation 
from datetime import date


class ReserveSerializer(serializers.Serializer ) : 
    class Meta : 
        model = Reservation 
        fields = ["day" , "type" , "date" , "time" , "id"]


    def validate_date(self, attrs):
        if date.today > attrs : 
            return serializers.ValidationError("date is not accessable")
        return attrs
    
class DaySerializer(serializers.Serializer) : 
    date = serializers.DateField()    
    doctor_id = serializers.IntegerField()
    
class BetweenDatesSerializer(serializers.Serializer):
    start_date = serializers.DateField()
    end_date = serializers.DateField()
    doctor_id = serializers.IntegerField()