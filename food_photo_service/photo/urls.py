from django.urls import path
from .views import upload_photo, view_photo, homepage_view

urlpatterns = [
    path("upload/", upload_photo, name="upload_photo"),
    path('', homepage_view, name='homepage'),  # This handles food-photo/
    path('view/', view_photo,  name='view_photo'),

]
