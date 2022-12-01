from email import message
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class OwnerProfilePhoto(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owner_profile_photo')
    picture = models.BinaryField(null=True, editable=True, blank=True)
    content_type = models.CharField(max_length=256, null=True, help_text='The MIMEType of the file', blank=True)

class Chat(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender_chat')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver_chat')

    class Meta:
         unique_together =   ('sender','receiver')

class UserMessage(models.Model):
    text = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE, related_name='user_message')