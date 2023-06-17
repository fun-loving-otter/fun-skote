from django.urls import path
from main.tests.views import LimitedActionView, LimitedActionView2



urlpatterns = [
    path('limited-action-view/', LimitedActionView.as_view(), name='limited-action-view'),
    path('limited-action-view2/', LimitedActionView2.as_view(), name='limited-action-view2'),
]
