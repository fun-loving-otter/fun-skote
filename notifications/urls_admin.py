from django.urls import path

from notifications.views import NotificationCreateView

urlpatterns = [
    path('notification/create/', NotificationCreateView.as_view(), name='notification-create'),
]
