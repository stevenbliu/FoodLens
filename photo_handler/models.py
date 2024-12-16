from django.db import models
from django.utils import timezone

class Photo(models.Model):
    # Metadata about the photo
    filename = models.CharField(max_length=255)  # Filename as saved in S3
    file_size = models.PositiveIntegerField()  # File size in bytes
    s3_url = models.URLField()  # The S3 URL to access the photo
    upload_time = models.DateTimeField(default=timezone.now)  # Time when the photo metadata is saved
    # checksum = models.CharField(max_length=255, blank=True, null=True)  # Optional field to store checksum (e.g., MD5) 

    # Information about food (optional in the initial model)
    food_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Photo {self.id} - {self.filename}"

    class Meta:
        ordering = ['-upload_time']
