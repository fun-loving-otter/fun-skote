from django.contrib import messages
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from django.views.generic import CreateView

from control_panel.mixins import AccessRequiredMixin
from notifications.models import Notification

User = get_user_model()


class NotificationCreateView(AccessRequiredMixin, CreateView):
    template_name = 'control/form.html'
    model = Notification
    fields = ['title', 'image', 'text']
    success_url = reverse_lazy('control_panel:notification-create')

    def form_valid(self, form):
        response = super().form_valid(form)

        # Add all users to notification.users
        form.instance.users.set(User.objects.all())

        # Show success message and redirect
        messages.success(self.request, "Notification sent successfully")
        return response
