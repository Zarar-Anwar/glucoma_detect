from django.urls import path
from rest_framework.urls import app_name

from website.views import HomeView, MenuView, GalleryView, ContactView, AboutView

app_name = "website"

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('menu/', MenuView.as_view(), name='menu'),
    path('gallery/', GalleryView.as_view(), name='gallery'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('about/', AboutView.as_view(), name='about'),
]
