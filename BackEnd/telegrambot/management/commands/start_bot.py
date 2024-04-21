import subprocess
from django.core.management.base import BaseCommand
import requests
from telegrambot.credentials import TELEGRAM_API_URL, URL , TOKEN 
from telegram.ext import Updater 
import datetime
from reservation.models import Reservation 
from datetime import time

class Command(BaseCommand):
    __name__ = "start_bot"
    help = 'Starts the Telegram bot process'
    def handle(self, *args, **options):
        q = Reservation.objects.all()
        # updater = Updater(TOKEN)  #token=TOKEN , use_context=True
        # job_queue = updater.job_queue
        # job_queue.run_daily(self.send_daily_message, time(hour=13 , minute=0 , second=0))
        self.send_daily_message()
        # updater.start_polling()
        # updater.idle()

    def send_message(self, method, data):
        return requests.post(TELEGRAM_API_URL + method, data)

    def send_daily_message(self ):
        """Function to send daily message to all users.
        """
        today = datetime.date.today()
        reserves = Reservation.objects.filter( date = today )
        if reserves.exists() : 
            for reserve in reserves : 
                p = reserve.pationt 
                d = reserve.psychiatrist
                accountP = p.telegramAccount 
                accountD = d.telegramAccount
                
                if accountD :
                    doctor_msg = f'شما امروز یک رزرو با اطلاعات زیر دارید.\n زمان :{reserve.time} '
                    
                    self.send_message("sendMessage", {
                        'chat_id': accountD.chat_id,
                        'text': doctor_msg 
                    })
                if accountP : 
                    print("doctor account : " , accountP.chat_id)
                    patient_msg = f'پیام یادآوری: \n نوبت رزرو شده شامل اطلاعات زیر است : \n زمان : {reserve.time} \n دکتر : {d.get_fullname()}'
                    self.send_message("sendMessage", {
                        'chat_id': accountP.chat_id,
                        'text': patient_msg 
                    })
        else : 
            print("there is no reservation")




