from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from photo_handler.models import Photo

class BaseTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.photo_url = reverse('create_photo')  # Update with your actual URL name
        self.mock_data = {
            'filename': 'test_image.png',
            'file_size': 1024,
        }

class CreatePhotoViewTests(BaseTestCase):
    def test_create_photo_success(self):
        """Test creating a photo successfully"""
        response = self.client.post(self.photo_url, self.mock_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('url', response.data)
        self.assertIn('id', response.data)
        self.assertTrue(Photo.objects.filter(filename=self.mock_data['filename']).exists())

    def test_create_photo_missing_data(self):
        """Test creating a photo with missing data"""
        response = self.client.post(self.photo_url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)

    def test_create_photo_invalid_file_size(self):
        """Test creating a photo with invalid file size"""
        invalid_data = {'filename': 'invalid.png', 'file_size': -100}
        response = self.client.post(self.photo_url, invalid_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('file_size', response.data)

class PhotoDetailViewTests(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.photo = Photo.objects.create(filename='test_image.png', file_size=1024)
        self.detail_url = reverse('photo_detail', args=[self.photo.id])  # Update with your actual URL name

    def test_get_photo_success(self):
        """Test retrieving photo metadata successfully"""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['filename'], self.photo.filename)

    def test_get_photo_not_found(self):
        """Test retrieving photo metadata for a non-existent photo"""
        response = self.client.get(reverse('photo_detail', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('error', response.data)

import json

class SNSNotificationHandlerViewTests(BaseTestCase):
    def test_notification_handling(self):
        """Test processing a valid SNS notification"""
        sns_message = {
            "Type": "Notification",
            "Message": json.dumps({"event": "s3:ObjectCreated:Put", "key": "test_image.png"}),
        }
        headers = {'x-amz-sns-message-type': 'Notification'}
        response = self.client.post(reverse('notifications'), sns_message, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_subscription_confirmation(self):
        """Test SNS subscription confirmation"""
        sns_message = {
            "Type": "SubscriptionConfirmation",
            "SubscribeURL": "https://mock-subscribe-url.com",
        }
        headers = {'x-amz-sns-message-type': 'SubscriptionConfirmation'}
        response = self.client.post(reverse('notifications'), sns_message, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_invalid_message_type(self):
        """Test invalid SNS message type"""
        sns_message = {"Type": "InvalidType"}
        headers = {'x-amz-sns-message-type': 'InvalidType'}
        response = self.client.post(reverse('notifications'), sns_message, format='json', **headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
