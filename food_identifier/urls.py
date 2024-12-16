from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('photo/', include('photo_handler.urls')),
    # path('data/', include('data_handler.urls')),
    # path('search/', include('search.urls')),
    path('photo-handler/', include('photo_handler.urls')),  # Include the photo_handler app's urls

]
