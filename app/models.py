from django.db import models

# Create your models here.


class AudioFiles(models.Model):
    audio_file = models.FileField(upload_to='audio/')
    uploaded_at = models.DateTimeField(auto_now_add=True)





class TextFiles(models.Model):
    text_file = models.FileField(upload_to='text/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
