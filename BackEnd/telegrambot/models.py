from typing import Iterable
from django.db import models
from accounts.models import User 
# Create your models here.
class TelegramAccount(models.Model) : 
    # user = models.ForeignKey(User , on_delete=models.CASCADE )
    is_varify = models.BooleanField(default=False )
    chat_id = models.CharField( unique= True , max_length=15 )
    varification_code = models.CharField( max_length=4 , blank=True , null=True )
    
        
    