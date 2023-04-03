from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class NotificationModel(models.Model):
    notification_msg = models.TextField() 
    concerned_tabel_key = models.TextField()
    broadcast_time = models.DateTimeField(auto_now=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reciver_notification")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_sender_notification")
    seen  = models.BooleanField(default=False)

    def __str__(self) -> str:
        return str(self.receiver)
    
class ChannelName(models.Model):
    channel_name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="channel_name")

    def __str__(self) -> str:
        return str(self.owner)