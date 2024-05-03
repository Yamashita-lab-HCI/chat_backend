from django.db import models

class Message(models.Model):
    username = models.CharField(max_length=100)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}: {self.text[:50]}"
