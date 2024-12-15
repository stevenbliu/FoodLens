# food_photo_service/photo/views.py
from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage

def upload_photo(request):
    if request.method == 'POST' and request.FILES['photo']:
        uploaded_file = request.FILES['photo']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)
        return JsonResponse({"message": "Photo uploaded successfully!", "file_url": file_url})
    return JsonResponse({"message": "Upload a photo"}, status=200)
