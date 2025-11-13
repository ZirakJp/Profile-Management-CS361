from rest_framework import generics, permissions
from .models import User, UploadedFile
from .serializers import UserSerializer, FileUploadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

class UploadFileView(generics.CreateAPIView):
    serializer_class = FileUploadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class EditUserProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response({
            'user_count': User.objects.count(),
            'file_count': UploadedFile.objects.count()
        })

class GlobalFeaturesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({'features': ['explore', 'search', 'view public profiles']})
