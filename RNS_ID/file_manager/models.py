from django.db import models

class EncryptedFile(models.Model):
    original_filename = models.CharField(max_length=255)
    s3_url = models.URLField()
    encryption_key = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)