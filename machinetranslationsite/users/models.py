from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pictures')


def __str__(self):
    return f'{self.user.username} profile'


class TranslationTask(models.Model):
    input_text = models.TextField()
    output_text = models.TextField()