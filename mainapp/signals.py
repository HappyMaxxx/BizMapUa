from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Evaluation

@receiver(post_save, sender=Evaluation)
@receiver(post_delete, sender=Evaluation)
def update_business_rating(sender, instance, **kwargs):
    instance.business.update_average_rating()