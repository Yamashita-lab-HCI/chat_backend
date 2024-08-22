from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone


class Room(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
class Message(models.Model):
    # message_id = models.AutoField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:50]}"
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    icon_color = models.CharField(max_length=7, default="#E42222")

class Chat(models.Model):
    username = models.CharField(max_length=100)
    question = models.TextField()
    answer = models.TextField()
    purpose = models.CharField(max_length=100, blank=True, null=True)  # 新しいフィールド
    room = models.CharField(max_length=100, blank=True, null=True)  # 新しいフィールド
    created_at = models.DateTimeField(default=timezone.now)  # auto_now_add=True を削除

    def __str__(self):
        return f"{self.username}: {self.question[:50]}..."