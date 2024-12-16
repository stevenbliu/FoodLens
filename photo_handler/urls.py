# photo_handler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('generate-presigned-url/<str:filename>/<int:file_size>/', views.generate_presigned_url, name='generate_presigned_url'),
]
