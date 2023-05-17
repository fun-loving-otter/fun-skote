from django.urls import path, include
from control_panel.views import index_views

urlpatterns = [
	path('', index_views.IndexView.as_view(), name='index'),
	path('', include('control_panel.urls')),
	path('authentication/', include('authentication.urls')),
]
