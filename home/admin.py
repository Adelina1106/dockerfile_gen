from django.contrib import admin
from .models import Dockerfile_templates, Dockerfile_explanations, Dockerfile_instructions

admin.site.register(Dockerfile_templates)
admin.site.register(Dockerfile_instructions)
admin.site.register(Dockerfile_explanations)

# Register your models here.
