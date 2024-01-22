from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('profile/', views.profile, name='profile'),
    path('update_username/', views.update_username, name='update_username'),
    path('update_email/', views.update_email, name='update_email'),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name='accounts/password_reset.html'),
         name='reset_password'),

    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_sent.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_form.html'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_done.html'),
         name='password_reset_complete'),
]