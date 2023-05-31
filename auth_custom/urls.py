from django.urls import path

from authentication import views
from auth_custom import views as custom_views


app_name = "authentication"

urlpatterns = [
	# Login views
	path('login', views.LoginView.as_view(), name='login'),
	path('logout', views.logout, name='logout'),
	path('login-inactive', custom_views.InactiveLoginCheckView.as_view(), name='login-inactive'),
	# Registration views
	path('register', custom_views.PaidRegisterView.as_view(), name='register'),
	path('register/package', custom_views.SubscriptionInitializeView.as_view(), name='payment-package'),
	path('register/success', views.RegisterSuccessView.as_view(), name='register-success'),
	# Password views
	path('password/change/', views.pwd_change, name='password-change'),
	path('password/change/done/', views.pwd_change_done, name='password-change-done'),
	path('password/reset', views.pwd_reset, name='recoverpw'),
	path('password/reset/done/', views.pwd_reset_done, name='password-reset-done'),
	path('password/reset/<uidb64>/<token>/', views.pwd_reset_confirm, name='password-reset-confirm'),
	path('password/reset/complete/', views.pwd_reset_complete, name='password-reset-complete'),
	# Email views
	path('email/change', views.EmailChangeRequestView.as_view(), name='email-change'),
	path('email/change/<token>/', views.EmailChangeTokenView.as_view(), name='email-change-token'),
]
