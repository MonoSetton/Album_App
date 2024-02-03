from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('upload_image', views.upload_image, name='upload_image'),
    path('delete_image/<str:pk>', views.delete_image, name='delete_image'),
    path('add_comment/<str:pk>', views.add_comment, name='add_comment'),
    path('delete_comment/<str:pk>', views.delete_comment, name='delete_comment'),
]