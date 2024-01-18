from django.urls import path
from . import views


urlpatterns = [
    path('signup', views.sign_up, name='signup'),
    path('profile', views.profile, name='profile'),
    path('update_profile/<str:pk>', views.update_profile, name='update_profile'),
]