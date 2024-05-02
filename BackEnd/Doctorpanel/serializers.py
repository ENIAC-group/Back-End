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
    

