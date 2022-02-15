from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EmployeeProfile, EmployerProfile, User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if instance.is_employer:
        EmployerProfile.objects.get_or_create(user=instance)
    else:
        EmployeeProfile.objects.get_or_create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.is_employer:
        instance.employer_profile.save()
    else:
        EmployeeProfile.objects.get_or_create(user=instance)
