from django.db import models

from django.contrib.auth.models import User

class UserFileHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class ImageText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #associates each image text with an user
    purpose = models.TextField(default="Default purpose")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# Create your models here.
