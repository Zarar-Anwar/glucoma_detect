from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL
# Create your models here.



class Images(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True, help_text='Images for Testing')

    def __str__(self):
        return f"Image ID: {self.id}"


class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=1000)

    def __str__(self):
        return f" Description ID :{self.id}"


class AI_Response(models.Model):
    image = models.ImageField(upload_to='images', null=True, blank=True, help_text='AI Response Image')
    result = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    userId= models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"AI Response ID {self.id}"
