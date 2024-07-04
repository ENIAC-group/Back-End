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
from google.apps import meet_v2 as meet
from datetime import datetime, timedelta
from google.auth.transport.requests import Request




class GoogleMeetCredentialsMixin:
    def authorize(self,request) -> Credentials:
        """Ensure valid credentials for calling the Meet REST API."""
        credentials = None

        if os.path.exists('token.json'):
            credentials = Credentials.from_authorized_user_file('token.json')

        if credentials is None:
            flow = InstalledAppFlow.from_client_secrets_file(
                GOOGLE_CLIENT_SECRETS_FILE,SCOPES)
            flow.run_local_server(port=0)
            credentials = flow.credentials

        if credentials and credentials.expired:
            credentials.refresh(Request())

        if credentials is not None:
            with open("token.json", "w") as f:
                f.write(credentials.to_json())

        return credentials




class GoogleMeetAPIView(APIView, GoogleMeetCredentialsMixin):  
    def post(self, request):
        credentials = self.authorize(request)

        serializer = GoogleMeetSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            reservation_id = validated_data['reservation_id']
            try:
                reservation = Reservation.objects.get(id=reservation_id)
                psychiatrist = reservation.psychiatrist
                patient = reservation.pationt
            except Reservation.DoesNotExist:
                return Response({"error": "Psychiatrist or Patient not found"}, status=status.HTTP_404_NOT_FOUND)

            start_time = datetime.strptime(str(reservation.date) + "T" + str(reservation.time), "%Y-%m-%dT%H:%M:%S")
            end_time = start_time + timedelta(hours=1)  # Adding 1 hour to the start time

            event = {
                "summary": f"Appointment with Dr.{psychiatrist.user.lastname}",
                "description": "Appointment with psychiatrist",
                "colorId": 1,
                "organizer": {"email": psychiatrist.user.email},
                "conferenceData": {
                    "createRequest": {
                        "requestId": str(uuid.uuid4()),
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                    }
                },
                "start": {"dateTime": start_time.isoformat(), "timeZone": "UTC"},
                "end": {"dateTime": end_time.isoformat(), "timeZone": "UTC"},
                "attendees": [
                    {"email": psychiatrist.user.email, "responseStatus": "accepted", "organizer": True},
                    {"email": patient.user.email, "responseStatus": "accepted"}
                ]
            }

            try:
                service = build("calendar", "v3", credentials=credentials)
                inserted_event = (
                    service.events()
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
                email_handler.send_GoogleMeet_Link(email_subject, [email_recipient], psychiatrist.user.lastname,
                                                   reservation.date, reservation.time, reservation.MeetingLink)
                return Response(inserted_event, status=status.HTTP_201_CREATED)
            except HttpError as error:
                print(f"Error in inserting calendar event: {error}")
                return Response({"error": "Failed to insert calendar event"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)