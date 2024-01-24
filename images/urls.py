from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('delete_image/<str:pk>', views.delete_image, name='delete_image'),
]