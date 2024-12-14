from django.urls import path
from . import views

urlpatterns = [
    path('upload-encrypt/', views.upload_and_encrypt, name='upload_and_encrypt'),
]
