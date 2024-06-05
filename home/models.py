from django.db import models

from django.contrib.auth.models import User

class UserFileHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# ARE DEJA CAMP ID PENTRU CA IL FACE DJANGO AUTOMAT
class ImageText(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) #associates each image text with an user
    purpose = models.TextField(default="Default purpose")
    name= models.TextField(default="Default name")
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class Dockerfile_instructions(models.Model):
    name = models.CharField(max_length=255)

    TYPE_CHOICES = (
        (1, 'Mandatory'),
        (2, 'Optional'),
    )
    type = models.IntegerField(choices=TYPE_CHOICES)

    TYPE_CHOICES_ENV = (
        (1, 'Yes'),
        (2, 'No'),
    )
    type_env = models.IntegerField(choices=TYPE_CHOICES_ENV)



class Dockerfile_explanations(models.Model):
    instruction = models.ForeignKey(Dockerfile_instructions, on_delete=models.CASCADE)
    explanation = models.TextField()
    examples = models.TextField(default="No examples available")
    options = models.TextField(default="No options available")
    summary_explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.URLField(blank=True)



# Create your models here.
