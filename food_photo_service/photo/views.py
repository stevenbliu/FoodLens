from django.http import JsonResponse
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage

def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        uploaded_file = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        return JsonResponse({"message": "Photo uploaded successfully!", "file_url": file_url})
    # return JsonResponse({"message": "Photo uploaded successfully!"})
    return render(request, 'photo/upload_photo_form.html')

def view_photo(request):
    if request.method == 'GET':
        # uploaded_file = request.FILES['photo']
        # fs = FileSystemStorage()
        # filename = fs.save(uploaded_file.name, uploaded_file)
        # file_url = fs.url(filename)
        return JsonResponse({"message": "Photo VIEWED1 successfully!"})
    # return JsonResponse({"message": "Photo uploaded successfully!"})
    return JsonResponse({"message": "Photo VIEWED2 successfully!"})

from django.shortcuts import render

from django.shortcuts import render
from django.http import HttpResponse
# from .forms import PhotoUploadForm  # Import the form class for uploading photos
from .models import Photo  # Import the model for photos

def homepage_view(request):
    # Handle file upload
    if request.method == 'POST' and request.FILES['photo']:
        uploaded_photo = request.FILES['photo']
        photo = Photo.objects.create(image=uploaded_photo)  # Assuming a model with an `image` field
        photo.save()
    # if request.method == 'GET' and request.FILES['photo']:
    #     return JsonResponse({"message": "Photo VIEWED successfully!"})


    # Get the most recent photo to display
    latest_photo = Photo.objects.last()

    return render(request, 'homepage.html', {'latest_photo': latest_photo})



# from django.template.loader import get_template
# from django.http import HttpResponse
# from django.conf import settings

# def upload_photo(request):
#     try:
#         # Print out the directories where Django is looking for templates
#         print("Template directories Django is using:")
#         for dir in settings.TEMPLATES[0]['DIRS']:
#             print(f"- {dir}")
        
#         # Try loading the template
#         get_template('photo/upload_photo_form.html')
#         return HttpResponse("Template found and loaded successfully!")
#     except Exception as e:
#         return HttpResponse(f"Template loading error: {e}")
