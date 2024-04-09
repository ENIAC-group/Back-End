from django.shortcuts import render

# Create your views here.
import json
import requests
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .credentials import TELEGRAM_API_URL

@csrf_exempt
def telegram_bot(request):
  if request.method == 'POST':
    message = json.loads(request.body.decode('utf-8'))
    chat_id = message['message']['chat']['id']
    text = message['message']['text']
    send_message("sendMessage", {
      'chat_id': f'your message {text}'
    })
  return HttpResponse('ok')

def send_message(method, data):
  return requests.post(TELEGRAM_API_URL + method, data)