from django.shortcuts import render
import os
from .credentials import TELEGRAM_API_URL , TOKEN

import telebot

# BOT_TOKEN = os.environ.get('BOT_TOKEN')

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    bot.reply_to(message, message.text)



bot.infinity_polling()

    # Create your views here.
# import json
# import requests
# from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt

# @csrf_exempt
# def telegram_bot(request):
#   if request.method == 'POST':
#     message = json.loads(request.body.decode('utf-8'))
#     chat_id = message['message']['chat']['id']
#     text = message['message']['text']
#     send_message("sendMessage", {
#       'chat_id': f'your message {text}'
#     })
#   return HttpResponse('ok')

# def send_message(method, data):
#   return requests.post(TELEGRAM_API_URL + method, data)
