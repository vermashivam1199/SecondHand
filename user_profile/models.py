from email import message
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OwnerProfilePhoto(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile_photo')
    picture = models.BinaryField(null=True, editable=True, blank=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file', blank=True)
