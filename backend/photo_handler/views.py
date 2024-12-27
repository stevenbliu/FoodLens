from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.conf import settings
import boto3
from .models import Photo
from .serializers import PhotoSerializer
from .sns_service import parse_s3_notification, subscribe_to_sns
import logging
import traceback
import requests

# Set up logging
logger = logging.getLogger(__name__)

# # DRF Views
# class GeneratePresignedURLView(APIView):
#     """Generates a pre-signed URL for S3 uploads and saves metadata."""
#     def post(self, request):
#         data = request.data
#         filename = data.get('filename')
#         file_size = data.get('file_size')

#         if not filename or not file_size:
#             raise ValidationError({'error': 'Missing filename or file_size'})

#         try:
#             # Generate the pre-signed URL
#             s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
#             presigned_url = s3_client.generate_presigned_url(
#                 'put_object',
#                 Params={
#                     'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
#                     'Key': filename,
#                     'ContentType': 'image/png',
#                     'ContentLength': file_size,
#                 },
#                 ExpiresIn=3600,
#             )

#             # Save metadata to the database
#             serializer = PhotoSerializer(data={'filename': filename, 'file_size': file_size})
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'url': presigned_url}, status=status.HTTP_201_CREATED)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             logger.error(f"Error generating pre-signed URL: {traceback.format_exc()}")
#             return Response({'error': 'Server error', 'details': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class SNSNotificationHandlerView(APIView):
#     """Handles incoming SNS notifications."""
#     def post(self, request):
#         body = request.data
#         sns_message_type = request.headers.get("x-amz-sns-message-type", None)

#         if sns_message_type == "SubscriptionConfirmation":
#             subscribe_url = body.get("SubscribeURL")
#             if subscribe_url:
#                 response = requests.get(subscribe_url)
#                 if response.status_code == 200:
#                     return Response({"message": "Subscription confirmed successfully!"})
#                 return Response({"message": "Failed to confirm subscription!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#         elif sns_message_type == "Notification":
#             message = body.get('Message')
#             if isinstance(message, str):
#                 parsed_message = parse_s3_notification(message)
#                 logger.info(f"Notification received: {parsed_message}")

#                 serializer = PhotoSerializer(data={
#                     'filename': parsed_message['object_key'],
#                     'file_size': parsed_message['object_size'],
#                 })
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response({"message": "Notification processed successfully!"}, status=status.HTTP_200_OK)
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response({"error": "Invalid SNS message type"}, status=status.HTTP_400_BAD_REQUEST)

# class SNSSubscribeView(APIView):
#     """Subscribes to the SNS topic."""
#     def get(self, request):
#         topic_arn = settings.AWS_SNS_S3_OBJECT_PUT_NOTIFS
#         url_forward = f'https://{settings.ALLOWED_HOSTS[0]}'
#         endpoint = f"{url_forward}/photo-handler/sns_endpoint/"
#         response = subscribe_to_sns(topic_arn, endpoint)

#         if response:
#             return Response({"message": "Successfully subscribed!"})
#         return Response({"message": "Subscription failed!"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# class StoreImageDataView(APIView):
#     """Handles storing additional image data."""
#     def post(self, request):
#         serializer = PhotoSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'success': True, 'id': serializer.instance.id}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# class InjectTestDataView(APIView):
#     """Simulates injecting data into the database for testing purposes."""
    
#     def post(self, request, *args, **kwargs):
#         try:
#             # Example data to insert
#             test_data = {
#                 "filename": "test_image.jpg",
#                 "file_size": 1024,
#             }

#             # Serialize and save the test data
#             serializer = PhotoSerializer(data=test_data)
#             if serializer.is_valid():
#                 serializer.save()
                
#                 # Log table details
#                 table_name = Photo._meta.db_table  # Get the name of the table
#                 logger.info(f"Test data injected into table: {table_name}")
#                 logger.info(f"Table fields: {', '.join([field.name for field in Photo._meta.fields])}")
#                 return Response({"message": "Test data injected successfully!"}, status=status.HTTP_201_CREATED)
#             else:
#                 return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.conf import settings
import boto3
from .models import Photo
from .serializers import PhotoSerializer

class CreatePhotoView(APIView):
    """Handles creating a photo and generating a presigned URL."""
    
    def post(self, request):
        data = request.data
        filename = data.get('filename')
        file_size = data.get('file_size')

        if not filename or not file_size:
            raise ValidationError({'error': 'Missing filename or file_size'})

        try:
            # Generate presigned URL
            s3_client = boto3.client('s3', region_name=settings.AWS_REGION)
            presigned_url = s3_client.generate_presigned_url(
                'put_object',
                Params={
                    'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                    'Key': filename,
                    'ContentType': 'image/png',
                    'ContentLength': file_size,
                },
                ExpiresIn=3600,
            )

            # Save metadata to the database
            serializer = PhotoSerializer(data={'filename': filename, 'file_size': file_size})
            if serializer.is_valid():
                photo = serializer.save()
                return Response({'id': photo.id, 'url': presigned_url}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PhotoDetailView(APIView):
    """Handles retrieving metadata for a photo."""
    
    def get(self, request, id):
        try:
            photo = Photo.objects.get(id=id)
            serializer = PhotoSerializer(photo)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Photo.DoesNotExist:
            return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

class UploadPhotoView(APIView):
    """Optional view for tracking uploads (if not handled in frontend)."""
    
    def post(self, request, id):
        # Placeholder for upload tracking logic, if needed
        return Response({'message': 'Upload tracked successfully!'}, status=status.HTTP_200_OK)

class SNSNotificationHandlerView(APIView):
    """Handles SNS notifications for uploads."""
    
    def post(self, request, id):
        body = request.data
        sns_message_type = request.headers.get("x-amz-sns-message-type", None)

        if sns_message_type == "Notification":
            # Handle the S3 notification
            message = body.get('Message')
            if isinstance(message, str):
                # Parse and update database with upload status
                # Add your custom logic here
                return Response({"message": "Notification processed successfully!"}, status=status.HTTP_200_OK)

        return Response({"error": "Invalid SNS message type"}, status=status.HTTP_400_BAD_REQUEST)

class SNSSubscribeView(APIView):
    """Subscribes to the SNS topic."""
    
    def get(self, request):
        topic_arn = settings.AWS_SNS_S3_OBJECT_PUT_NOTIFS
        endpoint = f"https://{settings.ALLOWED_HOSTS[0]}/photos/upload-notification/"
        response = subscribe_to_sns(topic_arn, endpoint)

        if response:
            return Response({"message": "Successfully subscribed!"})
        return Response({"message": f"Subscription failed! Endpoint: {endpoint}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InjectTestDataView(APIView):
    """Injects test data into the database."""
    
    def post(self, request):
        test_data = {"filename": "test_image.jpg", "file_size": 1024}
        serializer = PhotoSerializer(data=test_data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Test data injected successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
