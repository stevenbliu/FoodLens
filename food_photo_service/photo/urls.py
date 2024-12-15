from django.urls import path
from .views import upload_photo

urlpatterns = [
    path("upload/", upload_photo, name="upload_photo"),
    path('', upload_photo, name='upload_photo'),  # This handles food-photo/

]
