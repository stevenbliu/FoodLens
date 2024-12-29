from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status
from django.conf import settings
import boto3
from .models import Photo
from .serializers import PhotoSerializer
import logging
import traceback
import requests
from .sns_service import *

# Set up logging
logger = logging.getLogger(__name__)

class CreatePhotoView(APIView):
    """Handles creating a photo and generating a presigned URL."""
    
    def post(self, request):
        data = request.data
        filename = data.get('filename')
        file_size = data.get('file_size')

        if not filename or not file_size:
            logger.error("Missing filename or file_size in request data")
            raise ValidationError({'error': 'Missing filename or file_size'})

        try:
            logger.info(f"Generating presigned URL for file: {filename} with size: {file_size}")
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
            logger.info(f"Presigned URL generated: {presigned_url}")

            # Save metadata to the database
            serializer = PhotoSerializer(data={'filename': filename, 'file_size': file_size})
            if serializer.is_valid():
                photo = serializer.save()
                logger.info(f"Photo metadata saved successfully: {photo.id}")
                return Response({'id': photo.id, 'url': presigned_url}, status=status.HTTP_201_CREATED)
            logger.error(f"Failed to serialize photo data: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"Error occurred while creating photo: {traceback.format_exc()}")
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PhotoDetailView(APIView):
    """Handles retrieving metadata for a photo."""
    
    def get(self, request, id):
        try:
            logger.info(f"Retrieving photo metadata for photo ID: {id}")
            photo = Photo.objects.get(id=id)
            serializer = PhotoSerializer(photo)
            logger.info(f"Photo metadata retrieved: {photo.id}")
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Photo.DoesNotExist:
            logger.error(f"Photo not found with ID: {id}")
            return Response({'error': 'Photo not found'}, status=status.HTTP_404_NOT_FOUND)

class UploadPhotoView(APIView):
    """Optional view for tracking uploads (if not handled in frontend)."""
    
    def post(self, request, id):
        logger.info(f"Tracking upload for photo ID: {id}")
        # Placeholder for upload tracking logic, if needed
        return Response({'message': 'Upload tracked successfully!'}, status=status.HTTP_200_OK)

class SNSNotificationHandlerView(APIView):
    """Handles SNS notifications for uploads."""
    
    def post(self, request):
        body = request.data
        sns_message_type = request.headers.get("x-amz-sns-message-type", None)

        if sns_message_type == "Notification":
            # Handle the S3 notification
            message = body.get('Message')
            if isinstance(message, str):
                logger.info(f"Received SNS Notification: {message}")
                # Parse and update database with upload status
                parsed_message = parse_s3_notification(message)
                logger.info(f"Parsed SNS message: {parsed_message}")
                # Add your custom logic here
                return Response({"message": f"Notification processed successfully! \n {parsed_message}"}, status=status.HTTP_200_OK)
            logger.error("SNS message is not a string")
        else:
            logger.error(f"Invalid SNS message type: {sns_message_type}")

        return Response({"error": f"Invalid SNS message type - {sns_message_type}" }, status=status.HTTP_400_BAD_REQUEST)

class SNSSubscribeView(APIView):
    """Subscribes to the SNS topic."""
    
    def get(self, request):
        topic_arn = settings.AWS_SNS_S3_OBJECT_PUT_NOTIFS
        endpoint = f"https://{settings.ALLOWED_HOSTS[0]}/photos/upload-notification/"
        logger.info(f"Subscribing to SNS topic: {topic_arn} with endpoint: {endpoint}")
        response = subscribe_to_sns(topic_arn, endpoint)

        if response:
            logger.info("Successfully subscribed to SNS topic")
            return Response({"message": "Successfully subscribed!"})
        logger.error(f"Subscription failed! Endpoint: {endpoint}")
        return Response({"message": f"Subscription failed! Endpoint: {endpoint}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InjectTestDataView(APIView):
    """Injects test data into the database."""
    
    def post(self, request):
        test_data = {"filename": "test_image.jpg", "file_size": 1024}
        logger.info(f"Injecting test data: {test_data}")

        serializer = PhotoSerializer(data=test_data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Test data injected successfully: {test_data}")
            return Response({"message": "Test data injected successfully!"}, status=status.HTTP_201_CREATED)
        
        logger.error(f"Failed to inject test data: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
