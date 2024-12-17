# photo_handler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get-presigned-url/', views.generate_presigned_url, name='generate_presigned_url')
]
