# from django.shortcuts import render,redirect,get_object_or_404
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import os.path
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.apps import meet_v2
# from utils.project_variables import SCOPES ,GOOGLE_CLIENT_SECRETS_FILE
# import asyncio
# from asgiref.sync import sync_to_async
# from django.views import View
# from googleapiclient.discovery import build,Resource
# from reservation.models import Reservation
# from counseling.models import Pationt , Psychiatrist
# from reservation.models import Reservation
# import utils.email as email_handler 
# import uuid
# from typing import Optional, List, Dict, Any
# from datetime import datetime, timezone
# from googleapiclient.errors import HttpError
# from .serializer import GoogleMeetSerializer
# import json
# from rest_framework import serializers

# class GoogleMeetSerializer(serializers.Serializer):
#     client_id = serializers.CharField()
#     client_secret = serializers.CharField()
#     refresh_token = serializers.CharField()
#     # date = serializers.DateField()
#     # time = serializers.TimeField()
#     # psychiatrist_id = serializers.IntegerField()
#     # patient_id = serializers.IntegerField()
#     reservation_id = serializers.IntegerField()
    

#     def create(self, validated_data):
#         # client_id = validated_data['client_id']
#         # client_secret = validated_data['client_secret']
#         # refresh_token = validated_data['refresh_token']
#         # date = validated_data['date']
#         # time = validated_data['time']
#         # psychiatrist_id = validated_data['psychiatrist_id']
#         # patient_id = validated_data['patient_id']
#         reservation_id = validated_data['Reservation_id']
#         return {
#             # 'client_id': client_id,
#             # 'client_secret': client_secret,
#             # 'refresh_token': refresh_token,
#             # 'date': date,
#             # 'time': time,
#             # 'psychiatrist_id': psychiatrist_id,
#             # 'patient_id': patient_id
#             'reservation_id' :reservation_id,
#         }

#     def update(self, instance, validated_data):
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         return instance


# class GoogleMeetAPIView(APIView):
#     # def __init__(self, client_id: str, client_secret: str, refresh_token: str) -> None:
#     def __init__(self):
#         super().__init__()
#         self.client_id, self.client_secret, self.token_uri = self._load_credentials()

#     # def _load_credentials(self):
#     #     try:
#     #         with open('credentials.json', 'r') as f:
#     #             credentials = json.load(f)
#     #             installed_credentials = credentials.get('installed', {})
#     #             client_id = installed_credentials.get('client_id', None)
#     #             client_secret = installed_credentials.get('client_secret', None)
#     #             token_uri = installed_credentials.get('token_uri', None)
#     #             return client_id, client_secret, token_uri
#     #     except Exception as e:
#     #         print(f"Error loading credentials: {e}")
#     #         return None, None, None

#     def _get_service(self) -> Optional[Resource]:
#         if not all((self.client_id, self.client_secret, self.token_uri)):
#             print("Invalid credentials.")
#             return None
#         try:
#             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#             if not creds or not creds.valid:
#                 if creds and creds.expired and creds.refresh_token:
#                     creds.refresh(Request())
#                 else:
#                     flow = InstalledAppFlow.from_client_secrets_file(
#                         'credentials.json', SCOPES)
#                     creds = flow.run_local_server(port=0)
#                 # Save the credentials for the next run
#                 with open('token.json', 'w') as token:
#                     token.write(creds.to_json())

#             return build("calendar", "v3", credentials=creds)
#         except Exception as e:
#             print(f"Error in getting Google Calendar service: {e}")
#             return None
#     def _refresh_token(self): 
#         creds = None
#             # The file token.json stores the user's access and refresh tokens, and is
#             # created automatically when the authorization flow completes for the first
#             # time.
#         if os.path.exists('token.json'):
#             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
#             # If there are no (valid) credentials available, let the user log in.
#         if not creds or not creds.valid:
#             if creds and creds.expired and creds.refresh_token:
#                 creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     'credentials.json', SCOPES)
#                 creds = flow.run_local_server(port=0)
#                 # Save the credentials for the next run
#             with open('token.json', 'w') as token:
#                 token.write(creds.to_json())
#         return build("calendar", "v3", credentials=creds)


        

    
#     @staticmethod
#     def _prepare_utc_datetime_strings(date_str: str, time_str: str) -> tuple[str, str]:
#         try:
#             datetime_format = "%Y-%m-%dT%H:%M:%S"
#             start_datetime_str = f"{date_str}T{time_str}:00"
#             end_datetime_str = f"{date_str}T{time_str}:45"

#             start_datetime = datetime.strptime(start_datetime_str, datetime_format)
#             end_datetime = datetime.strptime(end_datetime_str, datetime_format)

#             start_utc = start_datetime.astimezone(timezone.utc).isoformat(
#                 timespec="milliseconds"
#             )
#             end_utc = end_datetime.astimezone(timezone.utc).isoformat(
#                 timespec="milliseconds"
#             )

#             return start_utc, end_utc
#         except ValueError as e:
#             print(f"Error in processing date and time strings: {e}")
#             return None, None

#     def _insert_calendar_event(
#         self, service: Resource, date: str, time: str, summary: str, description: str
#     ) -> Optional[dict]:
#         start_utc, end_utc = self._prepare_utc_datetime_strings(date, time)
#         if not start_utc or not end_utc:
#             print("Invalid start or end UTC time.")
#             return None

#         event = {
#             "summary": summary,
#             "description": description,
#             "colorId": 1,
#             "conferenceData": {
#                 "createRequest": {
#                     "requestId": str(uuid.uuid4()),
#                     "conferenceSolutionKey": {"type": "hangoutsMeet"},
#                 }
#             },
#             "start": {"dateTime": start_utc, "timeZone": "UTC"},
#             "end": {"dateTime": end_utc, "timeZone": "UTC"},
#         }

#         try:
#             inserted_event = (
#                 service.events()
#                 .insert(
#                     calendarId="primary",
#                     sendNotifications=True,
#                     body=event,
#                     conferenceDataVersion=1,
#                 )
#                 .execute()
#             )

#             return inserted_event
#         except HttpError as error:
#             print(f"Error in inserting calendar event: {error}")
#             return None
    
    
#     def post(self, request):
#         serializer = GoogleMeetSerializer(data=request.data)
#         if serializer.is_valid():
#             validated_data = serializer.validated_data
#             # psychiatrist_id = validated_data['psychiatrist_id']
#             # patient_id = validated_data['patient_id']
#             reservation_id = validated_data['reservation_id']

#             # Fetch psychiatrist and patient objects from their respective IDs
#             try:
#                 reservation= Reservation.objects.get(ide=reservation_id)
#                 psychiatrist = reservation.psychiatrist
#                 patient = reservation.pationt
#                 # psychiatrist = Psychiatrist.objects.get(id=psychiatrist_id)
#                 # patient = Pationt.objects.get(id=patient_id)
#             except (Reservation.DoesNotExist):
#                 return Response({"error": "Psychiatrist or Patient not found"}, status=status.HTTP_404_NOT_FOUND)

#             service = self._get_service()
#             if service is None:
#                 return Response({"error": "Failed to get Google Calendar service"}, status=status.HTTP_400_BAD_REQUEST)

#             # Prepare the event details
#             event = {
#                 "summary": "Psychiatrist Appointment",
#                 "description": "Appointment with psychiatrist",
#                 "colorId": 1,
#                 "conferenceData": {
#                     "createRequest": {
#                         "requestId": str(uuid.uuid4()),
#                         "conferenceSolutionKey": {"type": "hangoutsMeet"},
#                     }
#                 },
#                 "start": {"dateTime": reservation.date + "T" + reservation.time, "timeZone": "UTC"},
#                 # "start": {"dateTime": validated_data['date'] + "T" + validated_data['time'], "timeZone": "UTC"},
#                 # "end": {"dateTime": validated_data['date'] + "T" + validated_data['time'], "timeZone": "UTC"},
#                 "attendees": [
#                     {"email": psychiatrist.user.email, "responseStatus": "accepted", "organizer": True},
#                     {"email": patient.user.email, "responseStatus": "accepted"}
#                 ]
#             }

#             try:
#                 inserted_event = (
#                     service.events()
#                     .insert(
#                         calendarId="primary",
#                         sendNotifications=True,
#                         body=event,
#                         conferenceDataVersion=1,
#                     )
#                     .execute()
#                 )

#                 # # Create a reservation record
#                 # Reservation.objects.create(
#                 #     psychiatrist=psychiatrist,
#                 #     patient=patient,
#                 #     date=validated_data['date'],
#                 #     time=validated_data['time'],
#                 #     type="مجازی"  # Assuming virtual meetings are default
#                 # )
#                 reservation.MeetingLink = inserted_event.get('hangoutLink', '')
#                 reservation.save()

#                 return Response(inserted_event, status=status.HTTP_201_CREATED)
#             except HttpError as error:
#                 print(f"Error in inserting calendar event: {error}")
#                 return Response({"error": "Failed to insert calendar event"}, status=status.HTTP_400_BAD_REQUEST)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # def get(self, request, event_id):
#     #     service: Optional[Resource] = self._get_service()
#     #     if service is None:
#     #         return Response({"error": "Failed to get Google Calendar service"}, status=status.HTTP_400_BAD_REQUEST)

#     #     try:
#     #         event = service.events().get(calendarId="primary", eventId=event_id).execute()
#     #         return Response(event, status=status.HTTP_200_OK)
#     #     except HttpError as error:
#     #         print(f"An error occurred: {error}")
#     #         return Response({"error": "Failed to fetch event"}, status=status.HTTP_404_NOT_FOUND)

#     def put(self, request, event_id):
#         data = request.data
#         service: Optional[Resource] = self._get_service()
#         if service is None:
#             return Response({"error": "Failed to get Google Calendar service"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             event = service.events().get(calendarId="primary", eventId=event_id).execute()
#             event.update(data)
#             updated_event = (
#                 service.events()
#                 .update(calendarId="primary", eventId=event_id, body=event)
#                 .execute()
#             )
#             return Response(updated_event, status=status.HTTP_200_OK)
#         except HttpError as error:
#             print(f"An error occurred: {error}")
#             return Response({"error": "Failed to update event"}, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, event_id):
#         service: Optional[Resource] = self._get_service()
#         if service is None:
#             return Response({"error": "Failed to get Google Calendar service"}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             service.events().delete(calendarId="primary", eventId=event_id).execute()
#             return Response({"message": "Event deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
#         except HttpError as error:
#             print(f"An error occurred: {error}")
#             return Response({"error": "Failed to delete event"}, status=status.HTTP_400_BAD_REQUEST)



# # view = GoogleMeetAPIView(GOOGLE_CLIENT_SECRETS_FILE)


#     # def post(self, request):
#     #     # data = request.data
#     #     # date = data.get('date')
#     #     # time = data.get('time')
#     #     summary = "Psychiatrist Appointment"
#     #     description = "Appointment with psychiatrist"

#     #     # psychiatrist_id = data.get('psychiatrist_id')  # Assuming you send psychiatrist_id in the request
#     #     # patient_id = data.get('patient_id')  # Assuming you send patient_id in the request
#     #     serializer = GoogleMeetSerializer(data=request.data)
#     #     if serializer.is_valid():
#     #         validated_data = serializer.validated_data
#     #         psychiatrist_id = validated_data['psychiatrist_id']
#     #         patient_id = validated_data['patient_id']
#     #     # Fetch psychiatrist and patient objects from their respective IDs
#     #     try:
#     #         psychiatrist = Psychiatrist.objects.get(id=psychiatrist_id)
#     #         patient = Pationt.objects.get(id=patient_id)
#     #     except (Psychiatrist.DoesNotExist, Pationt.DoesNotExist):
#     #         return Response({"error": "Psychiatrist or Patient not found"}, status=status.HTTP_404_NOT_FOUND)

#     #     service: Optional[Resource] = self._get_service()
#     #     if service is None:
#     #         return Response({"error": "Failed to get Google Calendar service"}, status=status.HTTP_400_BAD_REQUEST)

#     #     # Prepare the event details
#     #     event = {
#     #         "summary": summary,
#     #         "description": description,
#     #         "colorId": 1,
#     #         "conferenceData": {
#     #             "createRequest": {
#     #                 "requestId": str(uuid.uuid4()),
#     #                 "conferenceSolutionKey": {"type": "hangoutsMeet"},
#     #             }
#     #         },
#     #         "start": {"dateTime": date + "T" + time, "timeZone": "UTC"},
#     #         "end": {"dateTime": date + "T" + time, "timeZone": "UTC"},
#     #         "attendees": [
#     #             {"email": psychiatrist.user.email, "responseStatus": "accepted", "organizer": True},
#     #             {"email": patient.user.email, "responseStatus": "accepted"}
#     #         ]
#     #     }

#     #     try:
#     #         inserted_event = (
#     #             service.events()
#     #             .insert(
#     #                 calendarId="primary",
#     #                 sendNotifications=True,
#     #                 body=event,
#     #                 conferenceDataVersion=1,
#     #             )
#     #             .execute()
#     #         )

#     #         # Create a reservation record
#     #         Reservation.objects.create(
#     #             psychiatrist=psychiatrist,
#     #             patient=patient,
#     #             date=date,
#     #             time=time,
#     #             type="مجازی"  # Assuming virtual meetings are default
#     #         )

#     #         return Response(inserted_event, status=status.HTTP_201_CREATED)
#     #     except HttpError as error:
#     #         print(f"Error in inserting calendar event: {error}")
#     #         return Response({"error": "Failed to insert calendar event"}, status=status.HTTP_400_BAD_REQUEST)







# # class GoogleMeetAuthView(APIView):

# #     def get(self, request, *args, **kwargs):
# #         creds = None
# #         # The file token.json stores the user's access and refresh tokens, and is
# #         # created automatically when the authorization flow completes for the first
# #         # time.
# #         if os.path.exists('token.json'):
# #             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# #         # If there are no (valid) credentials available, let the user log in.
# #         if not creds or not creds.valid:
# #             if creds and creds.expired and creds.refresh_token:
# #                 creds.refresh(Request())
# #             else:
# #                 flow = InstalledAppFlow.from_client_secrets_file(
# #                     'credentials.json', SCOPES)
# #                 creds = flow.run_local_server(port=0)
# #             # Save the credentials for the next run
# #             with open('token.json', 'w') as token:
# #                 token.write(creds.to_json())
# #         return redirect("CreateGoogleMeet")


# # class CreateGoogleMeetLinkView(APIView):
# #     pass

# # class SendGoogleMeetLinkView(APIView):
# #     def post(self, request, *args, **kwargs) : 
# #         subject = 'لینک جلسه مجازی '
# #         email_handler.send_GoogleMeet_Link(subject=subject)
# #         pass



# # class CreateSpaceView(APIView):
# #     """
# #     API view for creating a Google Meet space asynchronously.
# #     """
    
# #     def post(self, request):
# #         creds = None
# #         # The file token.json stores the user's access and refresh tokens, and is
# #         # created automatically when the authorization flow completes for the first
# #         # time.
# #         if os.path.exists('token.json'):
# #             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# #         # If there are no (valid) credentials available, let the user log in.
# #         if not creds or not creds.valid:
# #             if creds and creds.expired and creds.refresh_token:
# #                 creds.refresh(Request())
# #             else:
# #                 flow = InstalledAppFlow.from_client_secrets_file(
# #                     'credentials.json', SCOPES)
# #                 creds = flow.run_local_server(port=0)
# #             # Save the credentials for the next run
# #             with open('token.json', 'w') as token:
# #                 token.write(creds.to_json())
# #         try:
# #             # Create a Meet v2 client (assuming proper authentication)
# #             client = meet_v2.SpacesServiceClient()

# #             # Create the request object (no data required for creation)
# #             request = meet_v2.CreateSpaceRequest()

# #             # Make the asynchronous request
# #             response = client.create_space(request=request)

# #             # Handle successful response
# #             return Response(response, status=status.HTTP_201_CREATED)

# #         except Exception as e:
# #             # Handle any exceptions that may occur
# #             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





# # # class CreateSpaceView(APIView):
# # #     def create_space(self,request):
# # #         creds = None
# # #         # The file token.json stores the user's access and refresh tokens, and is
# # #         # created automatically when the authorization flow completes for the first
# # #         # time.
# # #         if os.path.exists('token.json'):
# # #             creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# # #         # If there are no (valid) credentials available, let the user log in.
# # #         if not creds or not creds.valid:
# # #             if creds and creds.expired and creds.refresh_token:
# # #                 creds.refresh(Request())
# # #             else:
# # #                 flow = InstalledAppFlow.from_client_secrets_file(
# # #                     'credentials.json', SCOPES)
# # #                 creds = flow.run_local_server(port=0)
# # #             # Save the credentials for the next run
# # #             with open('token.json', 'w') as token:
# # #                 token.write(creds.to_json())

        
# #         # creds = Credentials.from_authorized_user_file('token.json', SCOPES)

# #         # Create a client
# #     #     client = meet_v2.SpacesServiceClient(credentials=creds)

# #     #     # Initialize request argument(s)
# #     #     request = meet_v2.CreateSpaceRequest()

# #     #     # Make the request
# #     #     response =  client.create_space(request=request)

# #     #     # Handle the response
# #     #     return response

# #     # def post(self, request, *args, **kwargs):
# #     #     # Run the async function in the event loop
# #     #     # creds = GoogleMeetAuthView.as_view()(request, *args, **kwargs)
# #     #     # creds = GoogleMeetAuthView.as_view()(request)
# #     #     # Call the function asynchronously
# #     #     response = self.create_space(request)
# #     #     return Response(data=response, status=status.HTTP_200_OK)


# # # class CreateGoogleMeet(APIView):

# # #     def get (self , request , *args,**kwargs):

# # #         pass
# #     # def post(self, request, reservation_id, *args, **kwargs):
# #         # # Check if the request is from an authenticated doctor
# #         # if not request.user.is_authenticated or not request.user.role == 'doctor':
# #         #     return Response({'error': 'Unauthorized'}, status=401)

# #         # # Retrieve the reservation
# #         # reservation = get_object_or_404(Reservation, pk=reservation_id)

# #         # # Initialize Google Meet API service
# #         # creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# #         # service = build('meet', 'v1', credentials=creds)

# #         # # Prepare the request body for creating a new meeting
# #         # body = {
# #         #     'conferenceSolutionKey': {
# #         #         'type': 'hangoutsMeet'
# #         #     },
# #         #     'requestId': str(reservation_id),  # Use reservation ID as a unique identifier
# #         #     'status': {
# #         #         'statusCode': 'requested'
# #         #     },
# #         #     'conferenceData': {
# #         #         'createRequest': {
# #         #             'requestId': str(reservation_id),
# #         #             'conferenceSolutionKey': {
# #         #                 'type': 'hangoutsMeet'
# #         #             }
# #         #         }
# #         #     },
# #         #     'attendees': [
# #         #         {'email': Psychiatrist.user.email},  # Psychiatrist as host
# #         #         {'email': reservation.patient.user.email, 'role': 'GUEST', 'responseStatus': 'ACCEPTED'}  # Patient as guest
# #         #     ]
# #         # }

# #         # # Call the Google Meet API to create a new meeting
# #         # try:
# #         #     response = service.conferences().create(body=body).execute()
# #         #     meeting_link = response['conferenceData']['entryPoints'][0]['uri']
# #         #     # Optionally, you can save this meeting link to the reservation or send it to the patient via email or other means.
# #         #     return Response({'meeting_link': meeting_link}, status=201)
# #         # except Exception as e:
# #         #     return Response({'error': str(e)}, status=500)



# # # class CreateSpaceView(APIView):
# # #     def get(self, request):
# # #         creds = Credentials.from_authorized_user_file('token.json')
# # #         # Refresh the token if it's expired
# # #         if creds.expired:
# # #             creds.refresh(Request())
# # #         try:
# # #             client = build('meet', 'v1', credentials=creds)
# # #             request = meet_v2.CreateSpaceRequest()
# # #             response = client.create_space(request=request)
# # #             return Response({'meeting_uri': response.meeting_uri}, status=status.HTTP_200_OK)
# # #         except Exception as error:
# # #             return Response({'error': str(error)}, status=status.HTTP_400_BAD_REQUEST)
# #         # Initialize Google Meet API
# #             # creds = Credentials.from_authorized_user_file('token.json')  # You need to set up OAuth credentials
# #             # service = build('meet', 'v2', credentials=creds)

# #             # try:
# #             #     # Create meeting space
# #             #     meeting_space = service.spaces().create(body={}).execute()

# #             #     # Generate meeting link
# #             #     meeting_link = meeting_space['name']  # This might need to be adjusted based on the API response

# #             #     return Response({'meeting_link': meeting_link}, status=status.HTTP_200_OK)
# #             # except Exception as e:
# #             #     return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    

# #     #  def post(self, request, *args, **kwargs):
# #     #     # Create a client
# #     #     client = meet_v2.SpacesServiceAsyncClient()

# #     #     # Initialize request argument(s)
# #     #     request = meet_v2.CreateSpaceRequest(
# #     #     )

# #     #     # Make the request
# #     #     response =  client.create_space(request=request)

# #     #     # Handle the response
# #     #     print(response)



# # class GetSpaceView(APIView):
# #     async def post(self, request, *args, **kwargs):
# #         # Create a client
# #         client = meet_v2.SpacesServiceAsyncClient()

# #         # Initialize request argument(s)
# #         request = meet_v2.GetSpaceRequest(
# #             name="name_value",
# #         )

# #         # Make the request
# #         response = await client.get_space(request=request)

# #         # Handle the response
# #         print(response)


# # class EndSpaceView(APIView):
# #     async def post(self, request, *args, **kwargs):
# #         # Create a client
# #         client = meet_v2.SpacesServiceAsyncClient()

# #         # Initialize request argument(s)
# #         request = meet_v2.EndActiveConferenceRequest(
# #             name="name_value",
# #         )

# #         # Make the request
# #         await client.end_active_conference(request=request)



