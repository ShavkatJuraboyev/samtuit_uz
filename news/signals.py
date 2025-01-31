from django.contrib.admin.models import LogEntry
from django.db.models.signals import pre_save
from django.dispatch import receiver

@receiver(pre_save, sender=LogEntry)
def add_ip_to_log(instance, **kwargs):
    request = kwargs.get('request', None)

    if request:
        ip = getattr(request, "user_ip", "N/A")
        device = getattr(request, "user_agent", "N/A")

        if "IP:" not in instance.change_message:
            instance.change_message += f" | IP: {ip} | Device: {device}"
            instance.change_message = instance.change_message.strip()