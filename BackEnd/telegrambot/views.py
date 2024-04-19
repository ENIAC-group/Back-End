import json
import re
import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from .models import TelegramAccount
from .credentials import TELEGRAM_API_URL, URL , TOKEN , WEB_HOOK_URL
from accounts.models import User 
from counseling.models import Pationt, Psychiatrist
import utils.email as email_handler 
from rest_framework.response import Response
import random
from rest_framework import status 
from telegram.ext import Updater , CallbackContext
import datetime
from reservation.models import Reservation 
from datetime import time

email_pattern = r"email\s*/\s*([^<>@\s]+@[^<>@\s]+\.[^<>@\s]+)"
code_pattern = r"code\s*/\s*(\d{4})"

def set_webhook(request):
    response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + URL).json()
    return HttpResponse(f"{response}")

@csrf_exempt
def telegram_bot(request):
    if request.method == 'POST':
        update = json.loads(request.body.decode('utf-8'))
        handle_update(update)
        return HttpResponse('ok')
    else:
        return HttpResponseBadRequest('Bad Request')

def handle_update(update):
    chat_id = update['message']['chat']['id']
    text = update['message']['text']
    print( "chat id ----------------> " ,  chat_id )
    if text == "/start":
        handle_start_command(chat_id)
    elif text == "/verify":
        tel_chat = TelegramAccount.objects.filter( chat_id = chat_id ).first()
        if tel_chat : 
            if tel_chat.is_varify : 
                send_message("sendMessage", {
                'chat_id': chat_id,
                'text': 'این اکانت قبلا تایید شده.'   
                })
                return Response({"message" : "this email does not exist."} , status=status.HTTP_400_BAD_REQUEST)
        handle_verify_command(chat_id)
    else:
        
        handle_other_commands(chat_id, text)

def handle_start_command(chat_id):
    send_message("sendMessage", {
        'chat_id': chat_id,
        'text': 'به بات تلگرام اینیاک خوش آمدید. برای تایید حساب خود گزینه verify را از منو انتخاب کنید.' 
    })

def handle_verify_command(chat_id):
    send_message("sendMessage", {
        'chat_id': chat_id,
        'text': 'لطفا ایمیلتان را به صورت روبه رو وارد کنید \n email/<ایمیل >'  
    })

def handle_other_commands(chat_id ,text  ):
    match_email = re.search(email_pattern, text)
    match_code = re.search(code_pattern, text)
    if match_email or match_code : 
        tel_chat = TelegramAccount.objects.filter( chat_id = chat_id )
        if tel_chat : 
            if tel_chat.first().is_varify : 
                send_message("sendMessage", {
                'chat_id': chat_id,
                'text': 'این اکانت قبلا تایید شده.'   
                })
                return Response({"message" : "this email does not exist."} , status=status.HTTP_400_BAD_REQUEST) 
            
    if match_email:
        email = match_email.group(1)
        print("email ------> " , email )
        user = User.objects.filter(email__iexact = email.strip() ).first()
            
        if not user : 
            send_message("sendMessage", {
            'chat_id': chat_id,
            'text': 'ایمیل داده شده در میان کاربران موجود نمی باشد. لطفا ایمیل صحیح را وارد نمایید.'   
            })
            return Response({"message" : "this email does not exist."} , status=status.HTTP_400_BAD_REQUEST)
        
        elif ( user.is_email_verified == False) : 
            send_message("sendMessage", {
            'chat_id': chat_id,
            'text': 'ایمیل شما توسط سایت تایید نشده است. لطفا ابتدا ایمیل خود را در سایت کلنیک تایید کنید.'   
            })
            return Response({"message" : "this email does not varifyed in app."} , status=status.HTTP_400_BAD_REQUEST)
        
        else : 
 
           
            acc = TelegramAccount.objects.filter( chat_id = chat_id )
            if not acc.exists() : 
                verification_code = str(random.randint(1000, 9999))
                tel_account = TelegramAccount.objects.create( 
                    varification_code = verification_code , 
                    chat_id = chat_id 
                )

                if user.role == "doctor" : 
                    doctor = Psychiatrist.objects.filter( user = user )
                    if not doctor : 
                        return Response({"message" : "there is no doctor with this email ."} , status=status.HTTP_400_BAD_REQUEST) 
                    doctor = doctor.first()
                    doctor.telegramAccount = tel_account
                elif user.role == "user" : 
                    patient = Pationt.objects.filter( user = user )
                    print("117")
                    if not patient : 
                        return Response({"message" : "there is no patient with this email ."} , status=status.HTTP_400_BAD_REQUEST) 
                    patient = patient.first()
                    print( patient.pk)
                    patient.telegramAccount = tel_account
                    patient.save()

                    print("118")
                email_handler.send_telegram_account_verification_message( 
                    subject='تایید اکانت تلگرام' , 
                    recipient_list=[user.email ] , 
                    verification_token= verification_code , 
                )
                print("128")
                send_message("sendMessage", {
                    'chat_id': chat_id,
                    'text': 'کد تایید ارسال شده به ایمیلتان را به صورت روبه رو وارد کنید\n code/ <کد>.'   
                })

    elif match_code:
        tel_account = TelegramAccount.objects.filter(chat_id = chat_id ).first()
        if not tel_account : 
            return Response({"message" : "this chat_id is not varified by the Enic bot!"} , status=status.HTTP_400_BAD_REQUEST)
        else : 
            code = match_code.group(1)
            if tel_account.varification_code != code : 
                send_message("sendMessage", {
                'chat_id': chat_id,
                'text': 'کد وارد شده درست نمی باشد یا با فرمت خواسته شده وارد نشده.'   
                })    
                return Response({"message" : "varification code did not match"} , status=status.HTTP_400_BAD_REQUEST)
            else : 
                tel_account.is_varify = True 
                tel_account.varification_code = ''
                tel_account.save()

                send_message("sendMessage", {
                    'chat_id': chat_id,
                    'text': 'حساب شما با موفقیت تایید شد. رزروهای شما از طریق بات تلگرام به شما اطلاع رسانی خواهد شد.'   
                })

    else:
        send_message("sendMessage", {
            'chat_id': chat_id,
            'text': 'این پیام پشتیبانی نمیشود'  
        })


def setwebhook(request) : 
    if request.method == 'GET' : 
        return requests.get(url=WEB_HOOK_URL )


def send_message(method, data):
    return requests.post(TELEGRAM_API_URL + method, data)




