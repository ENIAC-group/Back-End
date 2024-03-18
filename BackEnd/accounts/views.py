from django.http import HttpResponse
from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import  Response
from rest_framework.views import APIView 
from rest_framework.generics import CreateAPIView , GenericAPIView
from .serializers import   UserSerializer   , LoginSerializer 
from .models import User
from datetime import datetime
from django.contrib.sites.shortcuts import get_current_site
from .utils import generate_tokens , EmailThread
import random
from django.conf import settings
import utils.email as email_handler 
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
import random
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from utils.project_variables import MAX_VERIFICATION_TRIES



class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if user is not None:
            tokens = generate_tokens(user.id)

            login(request, user)

            return Response({
                'refresh': tokens['refresh'],
                'access': tokens['access'],
                'user': UserSerializer(user).data,
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        refresh_token = request.COOKIES.get('token')

        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(data={'detail': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

            response = Response(data={'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)
            response.delete_cookie('refresh_token')
            response.delete_cookie('access_token')
            return response

        if request.user.is_authenticated:
            logout(request)
            return Response(data={'detail': 'Logged out successfully'}, status=status.HTTP_200_OK)

        return Response(data={'detail': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)

