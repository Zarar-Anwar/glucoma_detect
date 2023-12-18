from django.urls import path
from . import views


# Website URLS
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.website_about, name='about'),
    path('image/detection/', views.image_detection, name='image-detection'),
    path('image/test/<str:result>/<str:value>/<str:id>/', views.Test.as_view(), name='test'),
    # path('image/test/<result>/<value>/<id>/', views.Test.as_view(), name='test'),
]

# User Urls
urlpatterns += [
    path('user/login/', views.user_login, name='user-login'),
    path('user/signup/', views.user_signup, name='user-signup'),
    path('user/logout/', views.user_logout, name='user-logout'),
    path('user/records/delete/', views.records_delete, name='records-delete'),
]

# Doctor Urls
urlpatterns += [
    path('doctor/view/', views.doctor, name='doctor'),
    path('doctor/add/description/', views.description, name='description'),
]
