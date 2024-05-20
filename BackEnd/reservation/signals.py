from django.db.models.signals import post_save
from django.dispatch import receiver
from reservation.models import Reservation
from GoogleMeet.views import GoogleMeetAPIView  

@receiver(post_save, sender=Reservation)
def create_virtual_meeting(sender, instance, created, **kwargs):
    if created and instance.type == 'مجازی': 
        google_meet_api = GoogleMeetAPIView()
        google_meet_api.post(request=None ,data={"reservation_id": instance.id})
# ///