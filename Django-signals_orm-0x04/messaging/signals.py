from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Message, Notification, MessageHistory

@receiver(post_save, sender=Message)
def create_notification_on_new_message(sender, instance, created, **kwargs):
    if created:
        Notification.objects.create(user=instance.receiver, message=instance)

@receiver(pre_save, sender=Message)
def log_message_edit(sender, instance, **kwargs):
    if instance.pk:  # Only applies to existing messages
        try:
            old_instance = Message.objects.get(pk=instance.pk)
            if old_instance.content != instance.content:
                # Save the old content to history
                MessageHistory.objects.create(
                    message=old_instance,
                    old_content=old_instance.content
                )
                instance.edited = True  # Mark message as edited
        except Message.DoesNotExist:
            pass  # New message, no edit to log