from django.shortcuts import render
from rest_framework import viewsets, serializers
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status 
from counseling.models import Pationt , Psychiatrist 
from .serializer import ReserveSerializer
from .models import Reservation



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
        Pationt = Pationt.objects.filter( user = request.user )
        reserve = Reservation.objects.create(
            date = serializer.validated_data["date"] , 
            type = serializer.validated_data["type"] , 
            time = serializer.validated_data["time"] , 
            day = serializer.validated_data["day"] ,
            psychiatrist = doctor , 
            Pationt = Pationt 
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
        

    def retrieve(self, request, *args, **kwargs):
        
        return super().retrieve(request, *args, **kwargs)
    


    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)

# an example : 
# class CalendarViewSet(viewsets.ModelViewSet):
#     permission_classes = [IsDoctor]

#     def create(self, request):
#         Pationt = get_object_or_404(Pationt, ssn=request.data.get('ssn'))
#         user = request.user
#         doctor = Doctor.objects.get(user=user)
#         calendar_serializer = CalendarSerializer(data=request.data)
#         calendar_serializer.is_valid(raise_exception=True)
#         calendar = calendar_serializer.create(calendar_serializer.validated_data)
#         calendar.Pationt = Pationt
#         calendar.doctor = doctor
#         calendar.save()
#         return Response({'message': 'event created successfully'}, status=status.HTTP_200_OK)

#     def list_month(self, request):
#         queryset = Calendar.objects.all()
#         month = request.data.get('month')
#         year = request.data.get('year')
#         queryset = queryset.filter(date__year=year, date__month=month)
#         serializer = CalendarSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def list_week(self, request):
#         queryset = Calendar.objects.all()
#         day = int(request.data.get('day'))
#         month = int(request.data.get('month'))
#         year = int(request.data.get('year'))
#         steps = 7
#         saturday = datetime(year=year, month=month, day=day).date()
#         delta = timedelta(days=7)
#         number_of_days_month = cd.monthrange(year, month)[1]
#         days_date = {}
#         if day + steps - 1 <= number_of_days_month:
#             queryset = queryset.filter(date__year=year, date__month=month, date__day__gte=day,
#                                        date__day__lte=day + steps - 1)
#         else:
#             q1 = queryset.filter(date__year=year, date__month=month, date__day__gte=day,
#                                  date__day__lte=number_of_days_month)
#             q2 = []
#             if month != 12:
#                 q2 = queryset.filter(date__year=year, date__month=(month + 1) % 12,
#                                      date__day__lte=(day + steps - 1) % number_of_days_month)
#             else:
#                 q2 = queryset.filter(date__year=year + 1, date__month=(month + 1) % 12,
#                                      date__day__lte=(day + steps - 1) % number_of_days_month)
#             queryset = q1.union(q2, all=True)
#         date_dict = {}
#         for event in queryset:
#             if event.date in date_dict.keys():
#                 date_dict[event.date].append(
#                     {'title': event.event_type,
#                      'Pationt_fullname': event.Pationt.first_name + ' ' + event.Pationt.last_name,
#                      'ssn': event.Pationt.ssn,
#                      'startTime': event.start_time.hour, 'endTime': event.end_time.hour,
#                      'image': event.Pationt.picture.url,
#                      'day': event.day, 'gender': event.Pationt.gender, 'birth_date': event.Pationt.birth_date,
#                      'disease_title': event.Pationt.disease.first().title if event.Pationt.disease.exists() else None})
#                 continue
#             date_dict[event.date] = [
#                 {'title': event.event_type,
#                  'Pationt_fullname': event.Pationt.first_name + ' ' + event.Pationt.last_name,
#                  'ssn': event.Pationt.ssn,
#                  'startTime': event.start_time.hour, 'endTime': event.end_time.hour, 'image': event.Pationt.picture.url,
#                  'day': event.day, 'gender': event.Pationt.gender, 'birth_date': event.Pationt.birth_date,
#                  'disease_title': event.Pationt.disease.first().title if event.Pationt.disease.exists() else None}]

#         day_list = ['شنبه', 'یک‌شنبه', 'دو‌شنبه', 'سه‌شنبه', 'چهار‌شنبه', 'پنج‌شنبه', 'جمعه', ]
#         output = []
#         for key in date_dict.keys():
#             inner_dict = {'date': key, 'day': date_dict[key][0]['day'], 'schedule': date_dict[key]}
#             output.append(inner_dict)

#         for de in range(7):
#             if saturday + timedelta(de) not in date_dict.keys():
#                 output.append({'date': saturday + timedelta(de), 'day': day_list[de], 'schedule': []})

#         return Response(sorted(output, key=lambda x: x['date']))
