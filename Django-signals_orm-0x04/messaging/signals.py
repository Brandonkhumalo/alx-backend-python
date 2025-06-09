from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Message, Notification, MessageHistory

User = get_user_model()

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

@receiver(post_delete, sender=User)
def delete_user_related_data(sender, instance, **kwargs):
    # Delete messages where the user is sender or receiver
    user_messages = Message.objects.filter(sender=instance) | Message.objects.filter(receiver=instance)
    user_message_ids = user_messages.values_list('id', flat=True)

    # Delete associated message histories
    MessageHistory.objects.filter(message_id__in=user_message_ids).delete()

    # Delete the messages themselves
    user_messages.delete()

    # Delete notifications for the user
    Notification.objects.filter(user=instance).delete()