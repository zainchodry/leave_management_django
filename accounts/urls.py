from django.urls import path
from . views import *
from django.contrib.auth import views as auth_views
from . forms import *

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', logout, name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html', form_class=ForgetPasswordForm), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html', form_class=ResetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
