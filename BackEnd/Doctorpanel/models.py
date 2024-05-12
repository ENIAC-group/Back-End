from django.db import models
from counseling.models import Psychiatrist
from counseling.models import Pationt
from reservation.models import Reservation


class DoctorPanel(models.Model):
    psychiatrist = models.ForeignKey(Psychiatrist, on_delete=models.CASCADE)
    date = models.DateField(null=True)
    HOUR_CHOICES = [
    (f'{i:02d}:00', f'{i:02d}:00') for i in range(24)  ]

    time = models.TimeField(choices=HOUR_CHOICES, null=True)

    def __str__(self):
        return f"{self.psychiatrist} - {self.date} at {self.time}"
