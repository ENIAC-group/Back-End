from django.shortcuts import render
from rest_framework import viewsets
from reservation import views
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reservation, Psychiatrist
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Rating.views import RatingViewSet
from Rating.models import Rating
from django.db.models import Count, Avg
from .serializers import DoctorPanelSerializer
from datetime import datetime, timedelta



class DoctorPanelView(viewsets.ModelViewSet):
    serializer_class=DoctorPanelSerializer

    def get_rating(self, request):
        serializer = DoctorPanelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        psychiatrist_id=serializer.validated_data['psychiatrist_id']
        psychiatrist = Psychiatrist.objects.get(pk=psychiatrist_id)
        ratings = Rating.objects.filter(psychiatrist=psychiatrist)

        ratings_count = ratings.values('rating').annotate(count=Count('rating'))

        average_score = ratings.aggregate(average=Avg('rating'))['average']

        total_ratings_count = ratings.count()

        response_data = {
            'ratings_count': {choice[1]: 0 for choice in Rating.CHOICES},
            'average_score': average_score or 0,
            'total_ratings_count': total_ratings_count
        }

        # Update response data with actual ratings count
        for rating_count in ratings_count:
            response_data['ratings_count'][Rating.CHOICES[rating_count['rating'] - 1][1]] = rating_count['count']

        return Response(response_data)
    









    

