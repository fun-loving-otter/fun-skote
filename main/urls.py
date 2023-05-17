from django.urls import path


urlpatterns = [
	path('', lambda x: "ok", name='index'),
]
