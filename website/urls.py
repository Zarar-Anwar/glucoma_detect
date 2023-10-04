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
]

# Doctor Urls
urlpatterns +=[
    path('doctor/view/',views.doctor,name='doctor'),
    path('doctor/login/',views.CustomLoginView.as_view(),name='doctor-login'),
    path('doctor/logout/',views.doctorLogout,name='logout'),
    path('doctor/add/description/',views.description,name='description'),
    path('test/',views.random_image_predictions,name='test-image'),

]

