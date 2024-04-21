from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.apps import meet_v2
from utils.project_variables import SCOPES ,GOOGLE_CLIENT_SECRETS_FILE
import asyncio
from asgiref.sync import sync_to_async
from django.views import View
from googleapiclient.discovery import build,Resource
from reservation.models import Reservation
from counseling.models import Pationt , Psychiatrist
from reservation.models import Reservation
import utils.email as email_handler 
import uuid
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from googleapiclient.errors import HttpError
from .serializer import GoogleMeetSerializer
import json


class GoogleMeetAPIView(APIView):

    creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
    if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
                # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service= build("calendar", "v3", credentials=creds)

    def post(self,request):
        serializer = GoogleMeetSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            reservation_id = validated_data['reservation_id']
            try:
                reservation= Reservation.objects.get(id=reservation_id)
                psychiatrist = reservation.psychiatrist
                patient = reservation.pationt
            except(Reservation.DoesNotExist):
                return Response({"error": "Psychiatrist or Patient not found"}, status=status.HTTP_404_NOT_FOUND)
            # if request.user == psychiatrist.user:
            #     organizer = True
            # else:
            #     organizer = False

            event = {
                "summary": f"Appointment with Dr.{psychiatrist.user.lastname}",
                "description": "Appointment with psychiatrist",
                "colorId": 1,
                "conferenceData": {
                    "createRequest": {
                        "requestId": str(uuid.uuid4()),
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    }
                },
                "start": {"dateTime": str(reservation.date) + "T" + str(reservation.time), "timeZone": "UTC"},
                "end": {"dateTime": str(reservation.date) + "T" + str(reservation.time), "timeZone": "UTC"},
                # "organizer" :{"email": psychiatrist.user.email, "responseStatus": "accepted"},
                "attendees": [
                    {"email": psychiatrist.user.email, "responseStatus": "accepted", "organizer": True},
                    {"email": patient.user.email, "responseStatus": "accepted"}
                ]
            }
            try:
                inserted_event = (
                    self.service.events()
                    .insert(
                        calendarId="primary",
                        sendNotifications=True,
                        body=event,
                        conferenceDataVersion=1,
                    )
                    .execute()
                )
                reservation.MeetingLink = inserted_event.get('hangoutLink', '')
                reservation.save()
                email_subject = "Reservation Confirmation"
                email_recipient = patient.user.email
                email_handler.send_GoogleMeet_Link(email_subject, [email_recipient],reservation.psychiatrist.user.lastname,
                                                   reservation.date,reservation.time, reservation.MeetingLink)
                return Response(inserted_event, status=status.HTTP_201_CREATED)
            except HttpError as error:
                print(f"Error in inserting calendar event: {error}")
                return Response({"error": "Failed to insert calendar event"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
                 
