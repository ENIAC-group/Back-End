from typing import Iterable
from django.db import models
from counseling.models import Psychiatrist , Pationt 
from datetime import date

class Reservation(models.Model) : 
    DAY_CHOICES = [
        ('شنبه', 'شنبه'),
        ('یک‌شنبه', 'یک‌شنبه'),
        ('دو‌شنبه', 'دو‌شنبه'),
        ('سه‌شنبه', 'سه‌شنبه'),
        ('چهار‌شنبه', 'چهار‌شنبه'),
        ('پنج‌شنبه', 'پنج‌شنبه'),
        ('جمعه', 'جمعه'),
    ]

    RESERVE_CHOICES = [
        ('حضوری' , 'حضوری') ,
        ( 'مجازی' , 'مجازی')
    ]
    
    psychiatrist = models.ForeignKey(Psychiatrist, on_delete=models.CASCADE, related_name='psychiatrist_reservations')
    pationt = models.ForeignKey(Pationt, on_delete=models.CASCADE, related_name='pationt_reservations')
    date = models.DateField()
    time = models.TimeField()
    type = models.CharField(choices=RESERVE_CHOICES)
    day = models.CharField(max_length=10, choices=DAY_CHOICES , blank=True  )


    class Meta:
        unique_together = ['date', 'time']

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
            self.date = day_dict[day_num]

        return super().save()