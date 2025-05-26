from datetime import timezone

from django.db.models.signals import post_save
from django.dispatch import receiver

from cinemas.models import Booking


@receiver(post_save, sender=Booking)
def set_purchase_date_on_payment(sender, instance, created, **kwargs):
    print("\nutworzony/zmodyfikowany booking (info z signal)\n")
