from django.contrib import admin
from .models import TherapyTests , GlasserTest , MedicalRecord , TreatementHistory
admin.site.register(TherapyTests)
admin.site.register(GlasserTest)
admin.site.register(MedicalRecord)
admin.site.register(TreatementHistory)
# Register your models here.
