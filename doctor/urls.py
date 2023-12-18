from django.urls import path

from .views import DashboardView, ProfileView, SettingView

app_name = "doctor"

urlpatterns = [
    path('doctor/dashboard/', DashboardView.as_view(), name="dashboard"),

    path('doctor/profile/', ProfileView.as_view(), name="profile"),

    path('doctor/setting/', SettingView.as_view(), name="setting"),
]
