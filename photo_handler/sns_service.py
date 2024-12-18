# sns_service.py
import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3

@csrf_exempt
def send_sns_notification(request):
    print('send')
    sns = boto3.client('sns', region_name='us-east-1')
    try:
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:xxxxxxxxxxxx:your-topic',
            Message="Test notification from Django!",
            Subject="Test Subject"
        )
        return JsonResponse({"message": "Notification sent!", "response": response})
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

import boto3
from botocore.exceptions import ClientError

# Initialize SNS client
sns_client = boto3.client('sns', region_name='us-east-1')

def subscribe_to_sns(topic_arn: str, endpoint: str):
    try:
        response = sns_client.subscribe(
            TopicArn=topic_arn,
            Protocol='https',  # or 'http' if not using https
            Endpoint=endpoint  # The endpoint of your Django backend that handles SNS notifications
        )
        return response
    except ClientError as e:
        print(f"Error subscribing to SNS: {e}")
        return None
