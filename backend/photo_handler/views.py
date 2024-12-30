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

# class SNSNotificationHandlerView(APIView):
#     """Handles SNS notifications for uploads."""
    
#     def post(self, request):
#         try:
#             logger.info(f"SNSNotificationHandlerView received POST Request")
            
#             # Check the content type to handle it accordingly
#             content_type = request.headers.get('Content-Type', '')
#             if 'application/json' not in content_type:
#                 if 'text/plain' in content_type:
#                     try:
#                         # Try decoding the body as JSON (SNS may send as plain text)
#                         body = json.loads(request.body.decode('utf-8'))
#                     except json.JSONDecodeError as e:
#                         logger.error(f"Error decoding SNS message: {e}")
#                         return Response({"error": "Failed to decode SNS message"}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     logger.error(f"Unsupported Content-Type: {content_type}")
#                     return Response({"error": "Unsupported Content-Type"}, status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
#             else:
#                 body = request.data  # Use the parsed JSON if Content-Type is application/json
            
#             sns_message_type = request.headers.get("x-amz-sns-message-type", None)
#             logger.info(f"Received SNS Notification: {sns_message_type}")

#             if sns_message_type == "Notification":
#                 # Handle the S3 notification
#                 message = body.get('Message')
#                 if isinstance(message, str):
#                     logger.info(f"Received SNS Notification: {message}")
#                     try:
#                         parsed_message = json.loads(message)  # Ensure the message is parsed as JSON
#                         logger.info(f"Parsed SNS message: {parsed_message}")
#                         return Response({"message": f"Notification processed successfully! \n {parsed_message}"}, status=status.HTTP_200_OK)
#                     except json.JSONDecodeError as e:
#                         logger.error(f"Error parsing SNS message: {e}")
#                         return Response({"error": "Failed to parse SNS message"}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     logger.error("SNS message is not a string")
#                     return Response({"error": "SNS message is not a valid string"}, status=status.HTTP_400_BAD_REQUEST)

#             elif sns_message_type == "SubscriptionConfirmation":
#                 # Subscription confirmation: You need to confirm the subscription by calling the SubscribeURL
#                 sns_message = json.loads(request.body)
#                 subscribe_url = sns_message.get("SubscribeURL")
#                 logger.info ('Subscription Confirmation')

#                 if subscribe_url:
#                     response = requests.get(subscribe_url)
#                     if response.status_code == 200:
#                         logger.info("Subscription confirmed successfully")
#                         return Response({"message": "Subscription confirmed"}, status=status.HTTP_200_OK)
#                     else:
#                         logger.error(f"Failed to confirm subscription. Status Code: {response.status_code}")
#                         return Response({"error": "Failed to confirm subscription"}, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     logger.error("Missing SubscribeURL in SubscriptionConfirmation message")
#                     return Response({"error": "Missing SubscribeURL"}, status=status.HTTP_400_BAD_REQUEST)

#             else:
#                 logger.error(f"Invalid SNS message type: {sns_message_type} - Body: {body}")
#                 return Response({"error": f"Invalid SNS message type - {sns_message_type}"}, status=status.HTTP_400_BAD_REQUEST)

#         except Exception as e:
#             logger.error(f"Error processing SNS notification: {e}")
#             return Response({"error": "Failed to process SNS notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SNSNotificationHandlerView(APIView):
    """Handles SNS notifications for uploads."""
    
    def post(self, request):
        try:
            logger.info(f"SNSNotificationHandlerView received POST Request")
            
            # Handle the request based on the content type
            body, sns_message_type = self.parse_request(request)
            
            # Handle based on SNS message type
            if sns_message_type == "Notification":
                return self.handle_notification(body)
            elif sns_message_type == "SubscriptionConfirmation":
                return self.handle_subscription_confirmation(body)
            else:
                return self.handle_invalid_message_type(body)
        
        except Exception as e:
            logger.error(f"Error processing SNS notification: {e}")
            return Response({"error": "Failed to process SNS notification"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def parse_request(self, request):
        """Parse request based on content type."""
        content_type = request.headers.get('Content-Type', '')
        
        if 'application/json' in content_type:
            return request.data, request.headers.get("x-amz-sns-message-type", None)
        
        if 'text/plain' in content_type:
            try:
                body = json.loads(request.body.decode('utf-8'))
                return body, request.headers.get("x-amz-sns-message-type", None)
            except json.JSONDecodeError as e:
                logger.error(f"Error decoding SNS message: {e}")
                raise ValueError("Failed to decode SNS message")
        
        raise ValueError(f"Unsupported Content-Type: {content_type}")

    def handle_notification(self, body):
        """Handle SNS Notification message."""
        message = body.get('Message')
        if isinstance(message, str):
            try:
                parsed_message = json.loads(message)  # Parse the message JSON
                logger.info(f"Parsed SNS message: {parsed_message}")
                return Response({"message": "Notification processed successfully", "details": parsed_message}, status=status.HTTP_200_OK)
            except json.JSONDecodeError as e:
                logger.error(f"Error parsing SNS message: {e}")
                return Response({"error": "Failed to parse SNS message"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"error": "SNS message is not a valid string"}, status=status.HTTP_400_BAD_REQUEST)

    def handle_subscription_confirmation(self, body):
        """Handle SNS SubscriptionConfirmation message."""
        subscribe_url = body.get("SubscribeURL")
        if subscribe_url:
            response = requests.get(subscribe_url)
            if response.status_code == 200:
                logger.info("Subscription confirmed successfully")
                return Response({"message": "Subscription confirmed"}, status=status.HTTP_200_OK)
            else:
                logger.error(f"Failed to confirm subscription. Status Code: {response.status_code}")
                return Response({"error": "Failed to confirm subscription"}, status=status.HTTP_400_BAD_REQUEST)
        logger.error("Missing SubscribeURL in SubscriptionConfirmation message")
        return Response({"error": "Missing SubscribeURL"}, status=status.HTTP_400_BAD_REQUEST)

    def handle_invalid_message_type(self, body):
        """Handle invalid SNS message types."""
        logger.error(f"Invalid SNS message type: {body}")
        return Response({"error": "Invalid SNS message type"}, status=status.HTTP_400_BAD_REQUEST)

class SNSSubscribeView(APIView):
    """Subscribes to the SNS topic."""
    
    def get(self, request):
        # logger.info(f"Subscribing to SNS topic: ")
        # return Response({"message": f"Subscription failed!"}, status=status.HTTP_201_CREATED)


        topic_arn = settings.AWS_SNS_S3_OBJECT_PUT_NOTIFS
        endpoint = f"https://{settings.ALLOWED_HOSTS[0]}/photos/notifications/"
        logger.info(f"Subscribing to SNS topic: {topic_arn} with endpoint: {endpoint}")
        
        try:
            response = subscribe_to_sns(topic_arn, endpoint)

            if response:
                logger.info("Successfully subscribed to SNS topic")
                return Response({"message": "Successfully subscribed!"})
            logger.error(f"Subscription failed! Endpoint: {endpoint}")
            return Response({"message": f"Subscription failed! Endpoint: {endpoint}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.exception("Unexpected error during SNS subscription")
            return Response(
                {"error": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
            
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
