from django.db import models
from counseling.models import Psychiatrist
from counseling.models import Pationt
from reservation.models import Reservation
# Create your models here.


class DoctorPanel(models.Model):
    psychiatrist = models.ForeignKey(Psychiatrist, on_delete=models.CASCADE)
    reservations = models.ManyToManyField(Reservation)