from django.db import models

from django.db.models import UniqueConstraint
from django.contrib.auth.models import User

class UserFileHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    file = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

# ARE DEJA CAMP ID PENTRU CA IL FACE DJANGO AUTOMAT
class Dockerfiles(models.Model):
    id_dockerfile = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,) #associates each image text with an user
    purpose = models.CharField(default="Default purpose", max_length=255)
    name= models.CharField(default=purpose, max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_dockerfile', 'user'], name='unique_dockerfile_user')
        ]

class Dockerfile_instructions(models.Model):
    id_instruction = models.AutoField(primary_key=True)
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
    id_explanation = models.AutoField(primary_key=True)
    instruction = models.ForeignKey(Dockerfile_instructions, on_delete=models.CASCADE)
    explanation = models.TextField()
    examples = models.TextField(default="No examples available")
    options = models.TextField(default="No options available")
    summary_explanation = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    source = models.URLField(blank=True)
    class Meta:
        constraints = [
            UniqueConstraint(fields=['id_explanation', 'instruction'], name='unique_dockerfile_instruction')
        ]


class Dockerfile_templates(models.Model):
    id_template = models.AutoField(primary_key=True)
    template_name = models.CharField(max_length=255)
    template_purpose = models.CharField(max_length=255)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)



# Create your models here.
