from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .Serializer import  RatingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class RatingViewSet(APIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        if serializer.is_valid():
            pationt_id = request.user.id
            psychiatrist = serializer.validated_data['psychiatrist']

            if Rating.objects.filter(pationt=pationt_id, psychiatrist=psychiatrist).exists():
                return Response({'error': 'You have already rated this psychiatrist.'}, status=status.HTTP_400_BAD_REQUEST)
            
            pationt=Pationt.objects.get(pk=pationt_id)

            doctor_rate=Rating.objects.create(
                psychiatrist=psychiatrist,
                pationt=pationt,
                rating=serializer.validated_data['rating'],
                comments=serializer.validated_data['comments'],

            )
            doctor_rate.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)