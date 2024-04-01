from typing import Any
from django.db import models
from accounts.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError 

class Psychiatrist(models.Model ) : 
    TYPE_INDIVIDUAL = 'individual'
    TYPE_KIDS = "kids"
    TYPE_COUPLES = "couples"
    TYPE_TEEN  = "teen"
    TYPE_USER = "defualt"
    CHOICES = (
        (TYPE_INDIVIDUAL , "Individual") , 
        (TYPE_COUPLES , "Couples") , 
        (TYPE_KIDS , "Kids") , 
        (TYPE_TEEN , "Teen") 
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE )
    image = models.ImageField(upload_to='images/doctors/profile_pics', null=True, default='images/doctors/profile_pics/default.png')
    field = models.CharField( max_length=255, choices=CHOICES , default=TYPE_USER)

    def get_default_profile_image(self):
        if self.usesr.gender == 'M':
            return 'images/doctors/profile_pics/male_default.png'
        else:
            return 'images/doctors/profile_pics/female_default.png'

    def save(self, *args, **kwargs):
        if not self.user.role == 'doctor':
            self.user.role = User.TYPE_DOCTOR
            self.user.save()
        super().save(*args, **kwargs)

    @property
    def get_profile_image(self ) :
        if  not self.image : 
            return self.get_default_profile_image()
        else : 
            return self.image.url   # settings.MEDIA_ROOT +

    def get_fullname(self) :
        return self.user.firstname + " " + self.user.lastname 

    def save(self, *args, **kwargs):
        # Check if there's already a Psychiatrist object associated with this User
        if Psychiatrist.objects.filter(user=self.user).exists():
            raise ValidationError("A Psychiatrist object already exists for this User.")
        super().save(*args, **kwargs)

# TODO add fields for pationt 
class Pationt( models.Model ) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
