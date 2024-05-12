from rest_framework import serializers
from counseling.models import Psychiatrist
from reservation.models import Reservation

class DoctorPanelSerializer(serializers.Serializer):
    psychiatrist_id = serializers.IntegerField()
    class Meta :
        model = Psychiatrist
        fields = ["psychiatrist_id"]
    def validate(self, attrs):
        return super().validate(attrs) 
    

class ReservationListSerializer(serializers.ModelSerializer):
    class Meta :
        model = Reservation
        fields = ["date","day","time","type","MeetingLink","pationt"]
    def validate(self, attrs):
        return super().validate(attrs)