from django.db import models
from counseling.models import Pationt 

# نیاز به بقا	
# نیاز به عشق و تعلق خاطر	
# نیاز به آزادی	
# نیاز به قدرت	
# نیاز به تفریح

class GlasserTest(models.Model) : 
    love = models.FloatField( default=0.0 )
    survive = models.FloatField( default=0.0 )
    freedom = models.FloatField( default=0.0 )
    power = models.FloatField( default=0.0 )
    fun = models.FloatField( default=0.0 )

class TherapyTests(models.Model) : 
    pationt = models.ForeignKey(Pationt , on_delete=models.CASCADE )
    MBTItest = models.CharField( max_length=6 , blank=True )
    glasserTest = models.ForeignKey( GlasserTest , on_delete=models.DO_NOTHING  , null=True)
    

