import requests
from .credentials import TELEGRAM_API_URL, URL , TOKEN 
from telegram.ext import Updater 
import datetime
from reservation.models import Reservation 
from datetime import time

def send_message(method, data):
    return requests.post(TELEGRAM_API_URL + method, data)


def send_daily_message(context):
    """Function to send daily message to all users.
    """
    print("here")
    reserves = Reservation.objects.all()
    # accounts = TelegramAccount.objects.all()
    for reserve in reserves : 
        p = reserve.pationt 
        d = reserve.psychiatrist
        accountP = p.telegramAccount 
        accountD = d.telegramAccount
        doctor_msg = 'شما امروز در ساعت فلان یک ملاقات با بیمار بنام فلان دارید.'
        patient_msg = 'شما امروز با دکتر فلانی در زمان فلان یک ملاقات دارید.'
        send_message("sendMessage", {
            'chat_id': accountD.chat_id,
            'text': doctor_msg 
        })

        send_message("sendMessage", {
            'chat_id': accountP.chat_id,
            'text': patient_msg 
        })

def main():
    # Initialize the updater and job queue
    updater = Updater(token=TOKEN , use_context=True)
    job_queue = updater.job_queue

    # Add the daily job to the job queue
    job_queue.run_daily(send_daily_message, time(hour=8 , minute=0 , second=0), context='your_chat_id')
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()





