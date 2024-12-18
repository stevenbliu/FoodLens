# sns_service.py
import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import boto3

@csrf_exempt
def send_sns_notification(request):
    print(request.method)
    if request.method == "POST":
        try:
            # Parse JSON data from the body
            data = json.loads(request.body.decode('utf-8'))
            message = data.get('message', '')

            # Initialize SNS client
            sns = boto3.client('sns', region_name='us-east-1')

            # Send notification
            sns.publish(
                TopicArn='arn:aws:sns:us-east-1:509399626395:photoUploadAlert',
                Message=message,
                Subject='Upload Notification'
            )
            
            return JsonResponse({'status': 'success', 'message': 'Notification sent successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    else:
        return JsonResponse({'status': 'error', 'message': 'Only POST method is allowed'})

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
