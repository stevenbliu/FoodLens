from django.http import JsonResponse
import boto3
from botocore.exceptions import NoCredentialsError
from django.conf import settings

def generate_presigned_url(request, filename, file_size):
    # Here, filename and file_size are passed as arguments from the URL pattern
    s3_client = boto3.client(
        's3',
        aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
        aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        region_name=settings.AWS_REGION,
    )

    try:
        # Generate a pre-signed URL to upload a file to S3
        response = s3_client.generate_presigned_url('put_object',
                                                    Params={'Bucket': settings.AWS_STORAGE_BUCKET_NAME,
                                                            'Key': filename,
                                                            'ContentType': 'image/jpeg',  # or your required content type
                                                            'ContentLength': file_size},
                                                    ExpiresIn=3600)  # URL expires in 1 hour
        return JsonResponse({'url': response})

    except NoCredentialsError:
        return JsonResponse({'error': 'No credentials found'}, status=400)
