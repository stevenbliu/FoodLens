# photo_handler/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('get-presigned-url/', views.generate_presigned_url, name='generate_presigned_url'),
    path('store-image-data/', views.store_image_data, name='store_image_data'),
    path('upload-notification/', views.upload_notification, name='upload_notification'),
    path('sns_endpoint/', views.sns_endpoint, name='sns_endpoint'),
    path('subscribe_view/', views.subscribe_view, name='subscribe_view'),
        # path('send-sns-notification/', send_sns_notification, name='send_sns_notification'),

]
