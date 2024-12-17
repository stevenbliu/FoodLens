import boto3
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json

@csrf_exempt  # If you want to skip CSRF validation for the API endpoint
def generate_presigned_url(request):
    if request.method == 'POST':
        try:
            # Parse the JSON data from the request body
            data = json.loads(request.body)
            filename = data.get('filename')
            file_size = data.get('file_size')

            if not filename or not file_size:
                return JsonResponse({'error': 'Missing filename or file_size in the request body'}, status=400)

            # Initialize the S3 client
            s3_client = boto3.client('s3', region_name=settings.AWS_REGION)

            # Generate a pre-signed URL
            response = s3_client.generate_presigned_url('put_object',
                                                        Params={
                                                            'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                            'Key': filename,
                                                            'ContentType': 'image/jpeg',  # Adjust as necessary
                                                            'ContentLength': file_size
                                                        },
                                                        ExpiresIn=3600)  # URL expires in 1 hour
            print(filename, file_size)
            return JsonResponse({'url': response})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON data'}, status=400)

        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid HTTP method. Use POST.'}, status=405)
