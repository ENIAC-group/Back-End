from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from .Serializer import  RatingSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

class RatingViewSet(APIView):
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        serializer = RatingSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)