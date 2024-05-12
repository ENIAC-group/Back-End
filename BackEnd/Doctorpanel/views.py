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
from .serializers import DoctorPanelSerializer ,ReservationListSerializer , FreeTimeSerializer
from datetime import datetime, timedelta
from .models import DoctorPanel
from rest_framework import generics, status
from rest_framework.status import HTTP_404_NOT_FOUND




class DoctorPanelView(viewsets.ModelViewSet):
    serializer_class=DoctorPanelSerializer

    def get_rating(self, request,psychiatrist_id):
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id=serializer.validated_data['psychiatrist_id']
        try:
            psychiatrist = Psychiatrist.objects.get(pk=psychiatrist_id)
        except Psychiatrist.DoesNotExist:
            return Response({'error': 'Psychiatrist not found.'}, status=HTTP_404_NOT_FOUND)
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
    
    def ThisWeekResevations(self,request,psychiatrist_id):
        #for each date it shows the rervations from saturday to friday 
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id=request.data.get('psychiatrist_id')
        try:
            psychiatrist = Psychiatrist.objects.get(pk=psychiatrist_id)
        except Psychiatrist.DoesNotExist:
            return Response({'error': 'Psychiatrist not found.'}, status=HTTP_404_NOT_FOUND)
        today = timezone.now().date()
        days_to_saturday = (today.weekday() - 5) % 7
        start_of_week = today - timedelta(days=days_to_saturday)
        end_of_week = start_of_week + timedelta(days=6)
        reservations_this_week = Reservation.objects.filter(
            psychiatrist=psychiatrist,
            date__range=[start_of_week, end_of_week]
        ).order_by('date','time')
        reservation_serializer = ReservationListSerializer(reservations_this_week, many=True)
        return Response({'reservations_this_week': reservation_serializer.data})
    
    def NextWeekReservations(self, request,psychiatrist_id):
        #Reservation starting today to 7 days later 
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id = serializer.validated_data['psychiatrist_id']
        try:
            psychiatrist = Psychiatrist.objects.get(pk=psychiatrist_id)
        except Psychiatrist.DoesNotExist:
            return Response({'error': 'Psychiatrist not found.'}, status=HTTP_404_NOT_FOUND)
        today = timezone.now().date()
        end_date = today + timedelta(days=6)

        reservations_next_seven_days = Reservation.objects.filter(
            psychiatrist=psychiatrist,
            date__range=[today, end_date]
        ).order_by('date','time')
        reservation_serializer = ReservationListSerializer(reservations_next_seven_days, many=True)
        
        return Response({'reservations_next_seven_days': reservation_serializer.data})

    def PostFreeTime(self,request):
        serializer = FreeTimeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        # freetime = DoctorPanel.objects.filter(psychiatrist=request.user.psychiatrist)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
 


        

    

