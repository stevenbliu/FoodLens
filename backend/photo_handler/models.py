from django.db import models
from django.utils import timezone
from django.conf import settings

class Photo(models.Model):
    # Metadata about the photo
    filename = models.CharField(max_length=255)  # Filename as saved in S3
    file_size = models.PositiveIntegerField()  # File size in bytes
    upload_time = models.DateTimeField(default=timezone.now)  # Time when the photo metadata is saved
    food_name = models.CharField(max_length=255, blank=True, null=True, default=None)  # Information about food (optional)

    def s3_url(self):
        # Generate the S3 URL dynamically
        return f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.{settings.AWS_REGION}.amazonaws.com/{self.filename}"

    def save(self, *args, **kwargs):
        # Any additional logic to execute before saving the instance
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Photo {self.id} - {self.filename}"

    class Meta:
        ordering = ['-upload_time']
