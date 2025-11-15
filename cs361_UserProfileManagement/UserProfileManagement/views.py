from rest_framework import generics, permissions
from .models import User, UploadedFile, UploadedImage
from .serializers import UserSerializer, ImageRetrieveSerializer, ImageUploadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import base64
import requests

class UploadFileView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        file = serializer.validated_data['file']
        image_data = base64.b64encode(file.read()).decode('utf-8')

        payload = {
            "images": [
                {
                    "filename": file.name,
                    "image_data": image_data
                }
            ]
        }

        try:
            res = requests.post("http://localhost:5001/upload", json=payload)
            res.raise_for_status()

            user = request.user if request.user.is_authenticated else None
            UploadedImage.objects.create(
                user=user,
                filename=file.name,
                description=request.data.get("description", ""),
                source="friend-flask-service"
            )

            return Response(res.json(), status=res.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)
        
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


class GetImageView(APIView):
    def post(self, request):
        serializer = ImageRetrieveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        payload = {"filenames": serializer.validated_data["filenames"]}

        try:
            res = requests.post(f"{settings.IMAGE_SERVICE_URL}/get", json=payload)
            return Response(res.json(), status=res.status_code)
        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=200)

class UserDetailForAuthView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow Express to access this

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            return Response({
                "id": user.id,
                "username": user.username,
                "passwordHash": user.password,  # Django stores hashed password
                "roles": ["user"] 
            })
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Missing credentials"}, status=400)

        try:
            res = requests.post(f"{settings.EXPRESS_AUTH_URL}/login", json={"username": username, "password": password})
            res.raise_for_status()
            return Response(res.json(), status=200)
        except requests.exceptions.RequestException:
            return Response({"error": "Invalid credentials"}, status=401)


class ExpressPingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        payload = {"username": "trong", "password": "cs361"}
        try:
            res = requests.post(f"{settings.EXPRESS_AUTH_URL}/login", json=payload)
            res.raise_for_status()
            return Response(res.json(), status=200)
        except requests.exceptions.RequestException:
            return Response({"error": "Express login failed"}, status=502)
