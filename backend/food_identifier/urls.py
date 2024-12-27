from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('photo/', include('photo_handler.urls')),
    # path('data/', include('data_handler.urls')),
    # path('search/', include('search.urls')),
    path('photos/', include('photo_handler.urls')),  # Include the photo_handler app's urls
    # path('photo-handler'),  # Include the photo_handler app's urls

    # path('', include('food_identifier.urls')),  # Include food_identifier app's URLs (for generate-presigned-url)
]
# project_name/urls.py
from django.contrib import admin
from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('photo-handler/', include('photo_handler.urls')),  # Correctly include the photo_handler app's URLs
# ]
