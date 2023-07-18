from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Notification(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='notification_images/')
    users = models.ManyToManyField(User, related_name='notifications')

    class Meta:
        ordering = ['-created']


    def __str__(self):
        return self.title
