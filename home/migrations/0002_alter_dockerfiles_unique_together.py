# Generated by Django 4.2.9 on 2024-06-23 18:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='dockerfiles',
            unique_together={('id_dockerfile', 'user')},
        ),
    ]