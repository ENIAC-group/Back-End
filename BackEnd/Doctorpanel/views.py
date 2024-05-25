from django.shortcuts import render
from rest_framework import viewsets
from reservation import views
from rest_framework.views import APIView
from rest_framework.response import Response
from counseling.models import  Psychiatrist
from reservation.models import Reservation
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from Rating.views import RatingViewSet
from Rating.models import Rating
from django.db.models import Count, Avg
from .serializers import DoctorPanelSerializer ,ReservationListSerializer , FreeTimeSerializer
from datetime import datetime, timedelta
from .models import FreeTime
from rest_framework import generics, status
from rest_framework.status import HTTP_404_NOT_FOUND
from datetime import datetime, time
from rest_framework.permissions import IsAuthenticated





class DoctorPanelView(viewsets.ModelViewSet):
    serializer_class=FreeTimeSerializer
    permission_classes = [IsAuthenticated]


    def get_rating(self, request):
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id=serializer.validated_data['psychiatrist_id']
        try:
            psychiatrist = Psychiatrist.objects.get(user_id=request.user.id)
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
    
    def ThisWeekResevations(self,request):
        #for each date it shows the rervations from saturday to friday 
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id=request.data.get('psychiatrist_id')
        try:
            psychiatrist = Psychiatrist.objects.get(user_id=request.user.id)
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
    
    def NextWeekReservations(self, request):
        #Reservation starting today to 7 days later 
        # serializer = DoctorPanelSerializer(data=request.data)
        # serializer.is_valid(raise_exception=True)
        # psychiatrist_id = serializer.validated_data['psychiatrist_id']
        try:
            psychiatrist = Psychiatrist.objects.get(user_id=request.user.id)
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

    def PostFreeTime(self, request):
        serializer = FreeTimeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                psychiatrist = Psychiatrist.objects.get(user_id=request.user.id)
            except Psychiatrist.DoesNotExist:
                return Response({'error': 'Psychiatrist not found.'}, status=HTTP_404_NOT_FOUND)
            # psychiatrist = serializer.validated_data['psychiatrist']
            date = serializer.validated_data['date']
            time = serializer.validated_data['time']
            
            free_time = FreeTime.objects.create(
                psychiatrist=psychiatrist,
                date=date,
                time=time
            )
            
            free_time.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

    def GetAllFreeTime(self,request):
        try:
            psychiatrist = Psychiatrist.objects.get(user_id=request.user.id)
        except Psychiatrist.DoesNotExist:
            return Response({'error': 'Psychiatrist not found.'}, status=HTTP_404_NOT_FOUND)

        free_times = FreeTime.objects.filter(psychiatrist=psychiatrist).order_by('date','time')
        serializer = FreeTimeSerializer(free_times, many=True)
        return Response({'Free Time List':serializer.data}, status=status.HTTP_200_OK)
 


        

    

