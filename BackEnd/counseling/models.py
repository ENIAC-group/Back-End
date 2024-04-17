from typing import Any
from django.db import models
from accounts.models import User
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from django.core.exceptions import ValidationError 
from telegrambot.models import TelegramAccount

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
    telegramAccount = models.OneToOneField(TelegramAccount , on_delete=models.CASCADE,null=True ,blank=True )

    #  telegram account = models.one to one ( telegram account )
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
            VAR = settings.MEDIA_URL +  str(self.image  )
            print(VAR)
            return VAR
        
    def get_fullname(self) :
        return str(self.user.firstname) + " " + str(self.user.lastname)

    def save(self, *args, **kwargs):
        """
        Check if there's already a Psychiatrist object associated with this User
        """ 
        if self.user.role == 'doctor' : 
            return super().save(*args, **kwargs)
        if Psychiatrist.objects.filter(user=self.user).exists():
            raise ValidationError("A Psychiatrist object already exists for this User.")
        if Pationt.objects.filter(user=self.user).exists() :
            pationt = Pationt.objects.get(user=self.user)
            pationt.delete()
        if not self.user.role == 'doctor':
            self.user.role = User.TYPE_DOCTOR
            self.user.save()
        super().save(*args, **kwargs)



class Pationt( models.Model ) : 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    telegramAccount = models.OneToOneField(TelegramAccount , on_delete=models.CASCADE,null=True , blank=True ) 
    def save(self, *args, **kwargs):
        """
        Check if there's already a Pationt object associated with this User
        """ 
        if Pationt.objects.filter(user=self.user).exists():
            raise ValidationError("A Pationt object already exists for this User.")
        super().save(*args, **kwargs)



