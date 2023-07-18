from django.contrib.auth import get_user_model

User = get_user_model()


# Signal handler to delete notification when all users are removed
def handle_users_changed(sender, instance, action, reverse, model, pk_set, **kwargs):
    if action == 'post_remove' and not reverse and model == User and instance.users.count() == 0:
        instance.delete()
