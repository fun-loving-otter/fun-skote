from django.apps import AppConfig


class MainConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'main'

    def ready(self):
        from main.signals import subscription_made_callback
        from payments.models import subscription_paid
        subscription_paid.connect(subscription_made_callback)
