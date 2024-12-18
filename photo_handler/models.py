from django.db import models
from django.utils import timezone
from django.conf import settings

class Photo(models.Model):
    # Metadata about the photo
    filename = models.CharField(max_length=255)  # Filename as saved in S3
    file_size = models.PositiveIntegerField()  # File size in bytes
    s3_url = models.URLField(blank=True, null=True)  # The S3 URL to access the photo
    upload_time = models.DateTimeField(default=timezone.now)  # Time when the photo metadata is saved
    checksum = models.CharField(max_length=255, blank=True, null=True)  # Optional field to store checksum (e.g., MD5)
    food_name = models.CharField(max_length=255, blank=True, null=True)  # Information about food (optional)

    def save(self, *args, **kwargs):
        # Generate the s3_url dynamically
        if not self.s3_url:
            self.s3_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{self.filename}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo {self.id} - {self.filename}"

    class Meta:
        ordering = ['-upload_time']
