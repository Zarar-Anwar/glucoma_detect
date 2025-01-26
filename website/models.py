# models.py
from django.db import models


class MenuCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name='items', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)

    def __str__(self):
        return self.name


class GalleryItem(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='gallery_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class AboutUs(models.Model):
    title = models.CharField(max_length=255)
    story_title = models.CharField(max_length=255)
    story_content = models.TextField()
    video_title = models.CharField(max_length=255)
    video_url = models.URLField()
    bg_image = models.ImageField(upload_to='about_page/')

    def __str__(self):
        return self.title


# Model for Chef
class Chef(models.Model):
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=255)  # E.g., 'Chef', 'Sous Chef', etc.
    bio = models.TextField()
    image = models.ImageField(upload_to='chefs/')

    def __str__(self):
        return self.name


class WebsiteContent(models.Model):
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name
