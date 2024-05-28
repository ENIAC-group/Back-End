from rest_framework import viewsets, serializers
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Profile
from Profile.serializer import DoctorProfileSerializer
from rest_framework.permissions import IsAuthenticated


class RecomendationSysView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = DoctorProfileSerializer
    permission_classes = [IsAuthenticated]
    @action(detail=False, methods=['get'])
    def get_recomended_doctors(self, request):
        pass


