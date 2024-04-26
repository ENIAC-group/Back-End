from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from counseling.models import Pationt , Psychiatrist 
from .serializer import ReserveSerializer
from .models import Reservation
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from datetime import date


class ReservationView(viewsets.ModelViewSet ) : 
    """
    A viewset for reservation that provides `create()`, `retrieve()`, `update()`,
    `partial_update()`, `destroy()` and `list()` actions.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ReserveSerializer 

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class( data= request.data )
        serializer.is_valid(raise_exception=True)
    
        if not hasattr(request, 'user'):
            return Response({'message': 'user is not loged in'}, status=status.HTTP_400_BAD_REQUEST)
        
        doctor = request.data.get('doctor_id')
        pationt = Pationt.objects.filter( user = request.user )
        reserve = Reservation.objects.create(
            date = serializer.validated_data["date"] , 
            type = serializer.validated_data["type"] , 
            time = serializer.validated_data["time"] , 
            # day = serializer.validated_data["day"] ,
            psychiatrist = doctor , 
            Pationt = pationt 
        )
        response = {
            "reserve" : ReserveSerializer(reserve).data ,
            "message" : "reservation successfully created"
        }
        return Response( data=response , status=status.HTTP_201_CREATED)
    

    def destroy(self, request, *args, **kwargs):
        try:
            reservation_id = kwargs.get('pk')
            reservation = Reservation.objects.get(id=reservation_id)
            reservation.delete()
            return Response({"message": "Reservation successfully deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Reservation.DoesNotExist:
            return Response({"message": "Reservation not found"}, status=status.HTTP_404_NOT_FOUND)
        
    def list_month(self, request):
        queryset = Reservation.objects.all()
        month = request.data.get('month')
        year = request.data.get('year')
        queryset = queryset.filter(date__year=year, date__month=month)
        serializer = ReserveSerializer(queryset, many=True)
        return Response(serializer.data , status=status.HTTP_200_OK)
    
    def last_week( self , request ) : 
        # get the date of saturday 
        # day_dict = {
        #     0 : 'شنبه' , 
        #     1 : 'یکشنبه',
        #     2 : 'دوشنبه' , 
        #     3 : 'سه شنبه'  , 
        #     4 : 'چهارشنبه' , 
        #     5 : 'پنج‌شنبه' , 
        #     6 : 'جمعه'  
        # }
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        date1 = serializer.validated_data['date']
        doctor = serializer.validated_data['doctor_id']
        day = (date1.weekday() + 2)%7 
        saturday = date( day= date1.day- day , month=date1.month , year=date1.year)
        thirsday = date( day= saturday.day+5 , month=saturday.month , year=saturday.year)
        reservations = Reservation.objects.filter(date__range=[saturday, thirsday], psychiatrist=doctor)
        serializer = ReserveSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def between_dates(self, request):
        serializer = self.get_serializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        doctor_id = serializer.validated_data['doctor_id']

        try:
            doctor = Psychiatrist.objects.get(id=doctor_id)
        except ObjectDoesNotExist:
            return Response({"message": "Doctor not found"}, status=status.HTTP_404_NOT_FOUND)

        if not start_date or not end_date:
            return Response({"message": "Both start_date and end_date are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            start_date = timezone.datetime.strptime(start_date, "%Y-%m-%d").date()
            end_date = timezone.datetime.strptime(end_date, "%Y-%m-%d").date()
        except ValueError:
            return Response({"message": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        reservations = Reservation.objects.filter(date__range=[start_date, end_date], psychiatrist=doctor)
        serializer = ReserveSerializer(reservations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)