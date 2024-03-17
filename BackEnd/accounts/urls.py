from .views import *
from django.urls import path


urlpatterns = [
    path('signup/' , SignUpView.as_view() , name='signup' ) ,
    path('activation_confirm/<str:token>/', ActivationConfirmView.as_view(), name='activation_confirm'),
    path('activation-resend/', ActivationResend.as_view(), name='activation-resend'),
]