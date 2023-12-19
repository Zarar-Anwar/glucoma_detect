from django.urls import path

from .views import DashboardView, ProfileView, SettingView, ReportHistoryView

app_name = "doctor"

urlpatterns = [
    path('doctor/dashboard/', DashboardView, name="dashboard"),

    path('doctor/report/history/', ReportHistoryView, name="report-history"),

    path('doctor/profile/', ProfileView.as_view(), name="profile"),

    path('doctor/setting/', SettingView.as_view(), name="setting"),
]
