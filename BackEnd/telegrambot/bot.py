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
    reserves = Reservation.objects.all()
    # accounts = TelegramAccount.objects.all()
    for reserve in reserves : 
        p = reserve.pationt 
        d = reserve.psychiatrist
        accountP = p.telegramAccount 
        accountD = d.telegramAccount
        p_name = p.get_fullname()
        d_name = d.get_fullname()
        timee = reserve.time 
        # pation_msg = f"امروز با دکتر با نام {d_name} درزمان {timee} ملاقات دارد"
        pation_msg = f"شما امروز با دکتر :\n"
        pation_msg += f"{d_name}\n"
        pation_msg += "در ساعت :\n"
        pation_msg += f"{reserve.time}\n"
        pation_msg += f"وقت ملاقات دارید."
        doctor_msg = f"در ساعت {timee} با مریض بنام {p_name} ملاقات"
        # Make sure to encode the messages using UTF-8
        pation_msg = pation_msg.encode('utf-8')
        doctor_msg = doctor_msg.encode('utf-8')
        # send_message("sendMessage", {
        #     'chat_id': accountD.chat_id,
        #     'text': doctor_msg 
        # })

        send_message("sendMessage", {
            'chat_id': accountP.chat_id,
            'text': pation_msg 
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





