from django.urls import path
from .views import UploadFileView, EditUserProfileView, AdminDashboardView, GlobalFeaturesView

urlpatterns = [
    path('files/upload/', UploadFileView.as_view()),
    path('users/me/', EditUserProfileView.as_view()),
    path('admin/dashboard/', AdminDashboardView.as_view()),
    path('global/features/', GlobalFeaturesView.as_view()),
]
