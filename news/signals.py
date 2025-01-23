from django.contrib.admin.models import LogEntry
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=LogEntry)
def add_ip_to_log(sender, instance, **kwargs):
    if hasattr(instance, 'request') and hasattr(instance.request, 'user_ip'):
        instance.change_message += f" | IP: {instance.request.user_ip}"
