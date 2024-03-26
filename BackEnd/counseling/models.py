from django.db import models
from accounts.models import User

class Psychiatrist(models.Model ) : 
    TYPE_INDIVIDUAL = 'individual'
    TYPE_KIDS = "kids"
    TYPE_COUPLES = "couples"
    TYPE_TEEN  = "teen"
    TYPE_USER = "defualt"

    CHOICES = (
        (TYPE_INDIVIDUAL , "Individual") , 
        (TYPE_COUPLES , "couples") , 
        (TYPE_KIDS , "Kids") , 
        (TYPE_TEEN , "Teen") 
    )
    image = models.ImageField(upload_to='images/profile_pics', default='images/profile_pics/default.png')
    type = models.CharField( max_length=255, choices=CHOICES , default=TYPE_USER)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    


# TODO add fields for pationt 
class Pationt( models.Model ) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
