from django.db import models

# Create your models here.

from django.contrib.auth.models import User

class Podcast(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    audio_file = models.FileField(upload_to='podcasts/')
    transcript_raw = models.TextField(blank=True, null=True) # AI Output
    transcript_final = models.TextField(blank=True, null=True) # Human Edited
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    detected_language = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title