from django.apps import AppConfig


class ChatsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'messaging'

class MessagingAppConfig(AppConfig):
    name = 'messaging'  # Change to your app's actual name

    def ready(self):
        import messaging_app.signals  # Adjust based on project structure
