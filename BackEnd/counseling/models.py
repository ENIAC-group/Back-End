from typing import Any
from django.db import models
from accounts.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError 

class Psychiatrist(models.Model ) : 
    TYPE_INDIVIDUAL = "فردی"
    TYPE_KIDS =  "کودک"
    TYPE_COUPLES = "زوج"
    TYPE_TEEN  = "نوجوان"
    TYPE_USER = "defualt"
    CHOICES = (
        (TYPE_INDIVIDUAL , "فردی") , 
        (TYPE_COUPLES , "زوج") , 
        (TYPE_KIDS , "کودک") , 
        (TYPE_TEEN , "نوجوان") 
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE )
    image = models.ImageField(upload_to='images/doctors/profile_pics', null=True,blank=True )  #, default='images/doctors/profile_pics/default.png')
    field = models.CharField( max_length=255, choices=CHOICES , default=TYPE_USER)

    def get_default_profile_image(self):
    
        if self.user.gender == 'M':
            res =  'images/doctors/profile_pics/male_default.png'   ## settings.MEDIA_URL + 
            return res
        else:
            res = 'images/doctors/profile_pics/female_default.png'
            return res

    def get_profile_image(self ) :
        if  not self.image : 
            var = self.get_default_profile_image()
            
            return var 
        else : 
            return settings.MEDIA_URL +  self.image  # settings.MEDIA_ROOT +

    def get_fullname(self) :
        return str(self.user.firstname) + " " + str(self.user.lastname)

    def save(self, *args, **kwargs):
        """
        Check if there's already a Psychiatrist object associated with this User
        """ 
        print( "hereeeeeeeeeeeeeeeeeeeeeeeeeeee")
        if Psychiatrist.objects.filter(user=self.user).exists():
            raise ValidationError("A Psychiatrist object already exists for this User.")
        if not self.user.role == 'doctor':
            self.user.role = User.TYPE_DOCTOR
            self.user.save()
        super().save(*args, **kwargs)


# TODO add fields for pationt 
class Pationt( models.Model ) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        """
        Check if there's already a Pationt object associated with this User
        """ 
        if Pationt.objects.filter(user=self.user).exists():
            raise ValidationError("A Pationt object already exists for this User.")
        super().save(*args, **kwargs)
