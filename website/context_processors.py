# context_processors.py
from .models import WebsiteContent


def website_content(request):
    website_content = WebsiteContent.objects.first()
    return {'website_content': website_content}
