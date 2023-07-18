from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'notifications'

    def ready(self):
        from notifications import signals
        from django.db.models.signals import m2m_changed
        from notifications.models import Notification

        # Connect the receiver to the m2m_changed signal
        m2m_changed.connect(
            signals.handle_users_changed,
            sender=Notification.users.through
        )
