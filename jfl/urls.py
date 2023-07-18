"""content_manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from django_email_verification import urls as email_urls


urlpatterns = [
    path('authentication/', include('authentication.urls')),
    path('', lambda request: redirect('main:data-list'), name='index'),
    path('', include('main.urls')),
    path('', include('core.urls')),
    path('affiliates/', include('affiliates.urls')),
    path('payments/', include('payments.urls')),
    path('features/', include('feature_requests.urls')),
    path('translations/', include('translations.urls')),
    path('email/', include(email_urls)),
]


if settings.DEBUG:
    from django.contrib import admin
    urlpatterns.append(path('admin/', admin.site.urls))

    # Handle static/media
    urlpatterns += static(settings.STATIC_URL)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # Allow handling of control urls on main domain in debug mode
    urlpatterns.append(path('control/', include('control_panel.urls')))
