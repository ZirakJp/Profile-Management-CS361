from django.urls import path, include
from .views import UploadFileView, EditUserProfileView, AdminDashboardView, GlobalFeaturesView ,GetImageView, UserDetailForAuthView, LoginView
from .views import ExpressPingView

urlpatterns = [
    path("api/auth/login/", LoginView.as_view()),
    path("api/test/express/", ExpressPingView.as_view()),
    path("api/users/<str:username>", UserDetailForAuthView.as_view()),
    path('upload-file/', UploadFileView.as_view(), name='upload-file'),
    path('files/upload/', UploadFileView.as_view(), name='upload-file'),
    path('files/get/', GetImageView.as_view(), name='get-image'),
    path('users/me/', EditUserProfileView.as_view(), name='edit-user-profile'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin-dashboard'),
    path('global/features/', GlobalFeaturesView.as_view(), name='global-features'),
]
