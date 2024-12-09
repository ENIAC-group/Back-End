from typing import Iterable
from django.db import models
from counseling.models import Psychiatrist , Pationt 
from datetime import date

class Reservation(models.Model) : 
    DAY0 = 'شنبه'
    DAY1 = 'یکشنبه'
    DAY2 = 'دوشنبه'
    DAY3 = 'سه‌شنبه'
    DAY4 = 'چهارشنبه'
    DAY5 = 'پنج‌شنبه'
    DAY6 = 'جمعه'

    DAY_CHOICES = [
        (DAY0 , 'شنبه' ),
        ( DAY1, 'یک‌شنبه'),
        ( DAY2 ,'دو‌شنبه'),
        (DAY3 ,'سه‌شنبه'),
        (DAY4 ,'چهار‌شنبه'),
        (DAY5 , 'پنج‌شنبه'),
        (DAY6 ,'جمعه')
    ]

    REMOTE = 'مجازی'
    INPERSON = 'حضوری'
    RESERVE_CHOICES = [
        (INPERSON , 'حضوری') ,
        ( REMOTE , 'مجازی')
    ]
    
    psychiatrist = models.ForeignKey(Psychiatrist, on_delete=models.CASCADE, related_name='psychiatrist_reservations')
    pationt = models.ForeignKey(Pationt, on_delete=models.CASCADE, related_name='pationt_reservations')
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(max_length=15 ,choices=RESERVE_CHOICES)
    day = models.CharField(max_length=10, choices=DAY_CHOICES , blank=True  )

    class Meta:
        unique_together = ['date', 'time' , 'pationt' , 'psychiatrist']

    def save(self, *args, **kwargs) :
        day_dict = {
            0 : 'دوشنبه' , 
            1 : 'سه شنبه'  , 
            2 : 'چهارشنبه' , 
            3 : 'پنج‌شنبه' , 
            4 : 'جمعه' , 
            5 : 'شنبه' , 
            6 : 'یکشنبه' 
        }

        if not self.day: 
            day_num = date.today().weekday()
            if day_dict[day_num] == self.DAY0 : 
                self.day = self.DAY0
            elif day_dict[day_num] == self.DAY1 : 
                self.day = self.DAY1
            elif day_dict[day_num] == self.DAY2 : 
                self.day = self.DAY2
            elif day_dict[day_num] == self.DAY3 : 
                self.day = self.DAY3
            elif day_dict[day_num] == self.DAY4 : 
                self.day = self.DAY4
            elif day_dict[day_num] == self.DAY5 : 
                self.day = self.DAY5
            else : 
                self.day = self.DAY6
        return super().save()