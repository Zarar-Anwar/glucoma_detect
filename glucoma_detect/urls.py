from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from glucoma_detect.settings import MEDIA_ROOT, STATIC_ROOT
from django.views.static import serve

"""ADMIN URLS ------------------------------------------------------------------------------------------------------"""

urlpatterns = [
    path('admin/', admin.site.urls)
]

"""WEBSITE URL -----------------------------------------------------------------------------------------------------"""

urlpatterns += [
    path('', include('website.urls')),
    path('', include('doctor.urls'))
]

""" STATIC AND MEDIA FILES ----------------------------------------------------------------------------------------- """
urlpatterns += [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': STATIC_ROOT}),
]
