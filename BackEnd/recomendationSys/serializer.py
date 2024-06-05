from rest_framework import serializers 
from .models import DoctorPersonalityInfo


class DoctorInfoSerializer( serializers.ModelSerializer ) : 
    class Meta : 
        model = DoctorPersonalityInfo
        fields = '__all__'
