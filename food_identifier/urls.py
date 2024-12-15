from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponseRedirect

urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the Django admin site
    path('food-photo/', include('food_photo_service.photo.urls')),  # Include URLs for photo service
    # path('food-info/', include('food_info_service.food_info.urls')),  # Include URLs for food info service (if needed)
    path('', lambda request: HttpResponseRedirect('/food-photo/')),  # Redirect the root to /food-photo/

]
