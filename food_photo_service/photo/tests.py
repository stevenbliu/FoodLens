from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
# from .models import Photo


class PhotoUploadTestCase(TestCase):
    
    def setUp(self):
        """Set up test data"""
        # This will run before each test method
        self.upload_url = reverse('upload_photo')  # URL for the upload view
        self.view_url = reverse('view_photo')  # URL for the upload view

    def test_upload_photo(self):
        """Test uploading a photo"""
        print('test upload')
        # Simulate uploading a file
        # with open('path/to/test/photo.jpg', 'rb') as photo_file:
            # file_data = SimpleUploadedFile("photo.jpg", photo_file.read(), content_type="image/jpeg")
        # response = self.client.post(self.upload_url, {'photo': 'photo1'})
        
        # Check if the response is valid (e.g., HTTP 200 OK or 201 Created)
        # self.assertEqual(response.status_code, 200)  # Adjust this based on your actual response status
        
        # Check if the photo was saved correctly
        # self.assertEqual(Photo.objects.count(), 1)
        # self.assertEqual(Photo.objects.first().image.name, 'photos/photo.jpg')  # Adjust based on your actual file path

        print(self.upload_url)
        
    def test_view_photo(self):
        """Test viewing a photo"""
        print('test view')
        # First, upload a photo to be viewed
        # with open('path/to/test/photo.jpg', 'rb') as photo_file:
        #     file_data = SimpleUploadedFile("photo.jpg", photo_file.read(), content_type="image/jpeg")
        #     self.client.post(self.upload_url, {'photo': file_data})
        
        # Now, view the uploaded photo
        # photo = Photo.objects.first()
        # view_url = reverse('view_photo', kwargs={'photo_id': photo.id})  # Adjust based on your URL pattern
        
        # response = self.client.get(view_url)
        # self.assertEqual(response.status_code, 200)  # Ensure that the response is valid
        # self.assertIn(photo.image.url, response.content.decode())  # Ensure the image URL is in the response

        print(self.view_url)
        response = self.client.get(self.view_url, {'photo': 123})
        self.assertEqual(response.status_code, 200)  # Ensure that the response is valid

        print(response.content.decode())

