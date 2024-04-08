from typing import Iterable
from django.db import models
from counseling.models import Psychiatrist , Pationt 


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
    day = models.CharField(max_length=10, choices=DAY_CHOICES)

    class Meta:
        unique_together = ['date', 'time']

    def save(self, *args, **kwargs) :
        return super().save()