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


class TranslationHistory(models.Model):
    source_text = models.TextField()
    target_text = models.TextField()
    source_language = models.CharField(max_length=255)
    target_language = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def clear_history(cls):
        cls.objects.all().delete()

    def __str__(self):
        return f"{self.source_text} -> {self.target_text}"
