from django.urls import path
from .views import UploadFileView, EditUserProfileView, AdminDashboardView, GlobalFeaturesView

urlpatterns = [
    path('files/upload/', UploadFileView.as_view(), name='upload-file'),
    path('users/me/', EditUserProfileView.as_view(), name='edit-user-profile'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('global/features/', GlobalFeaturesView.as_view(), name='global-features'),
]
