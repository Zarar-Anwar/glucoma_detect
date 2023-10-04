from django.urls import path
from . import views

# Website URLS
urlpatterns = [
    path('',views.home,name='home'),
    path('about/',views.website_about,name='about'),
]

# User Urls
urlpatterns +=[
    path('user/login/', views.user_login, name='user-login'),
    path('user/signup/', views.user_signup, name='user-signup'),
    path('user/logout/', views.user_logout, name='user-logout'),
]

# Doctor Urls
urlpatterns +=[
    path('doctor/view/',views.doctor,name='doctor'),
    path('doctor/add/description/',views.description,name='description'),
    path('test/',views.random_image_predictions,name='test-image'),

]

