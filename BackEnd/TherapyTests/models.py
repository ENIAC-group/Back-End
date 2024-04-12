from django.db import models
from counseling.models import Pationt 

class TherapyTests(models.Model) : 
    pationt = models.ForeignKey(Pationt , on_delete=models.CASCADE )
    MBTItest = models.CharField( max_length=6 , blank=True )
    


