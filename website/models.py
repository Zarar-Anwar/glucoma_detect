from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    is_user = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    email = models.EmailField(max_length=200, unique=True)
    REQUIRED_FIELDS = ['username', ]
    USERNAME_FIELD = 'email'

    class Meta:
        ordering = ['-id']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class Images(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True, help_text='Images for Testing')

    def __str__(self):
        return f"Image ID: {self.id}"


class AI_Response(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True, help_text='AI Response Image')
    result = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default=None, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_response_user')
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ai_response_doctor')

    def __str__(self):
        return f"AI Response ID {self.id}"
