from rest_framework import generics, permissions
from .models import User, UploadedFile, UploadedImage
from .serializers import UserSerializer, ImageRetrieveSerializer, ImageUploadSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

import base64
import requests


def call_image_service(url, payload, on_success=None):
    """Call an external image service and wrap the result in a DRF Response.

    Optionally executes `on_success(response)` if the request succeeds.
    """
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        if on_success is not None:
            on_success(response)
        return Response(response.json(), status=response.status_code)
    except requests.exceptions.RequestException as exc:
        return Response(
            {"error": str(exc)},
            status=status.HTTP_502_BAD_GATEWAY,
        )


class UploadFileView(APIView):
    def post(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        uploaded_file = serializer.validated_data["file"]
        image_data = self._encode_file_to_base64(uploaded_file)
        payload = self._build_upload_payload(uploaded_file.name, image_data)
        upload_url = f"{settings.IMAGE_SERVICE_URL}/upload"

        def record_uploaded_image(_response):
            self._record_uploaded_image(request, uploaded_file)

        return call_image_service(upload_url, payload, on_success=record_uploaded_image)

    def _encode_file_to_base64(self, uploaded_file):
        return base64.b64encode(uploaded_file.read()).decode("utf-8")

    def _build_upload_payload(self, filename, image_data):
        return {
            "images": [
                {
                    "filename": filename,
                    "image_data": image_data,
                }
            ]
        }

    def _record_uploaded_image(self, request, uploaded_file):
        user = request.user if request.user.is_authenticated else None
        UploadedImage.objects.create(
            user=user,
            filename=uploaded_file.name,
            description=request.data.get("description", ""),
            source="friend-flask-service",
        )


class EditUserProfileView(generics.UpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class AdminDashboardView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        return Response(
            {
                "user_count": User.objects.count(),
                "file_count": UploadedFile.objects.count(),
            }
        )


class GlobalFeaturesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response(
            {"features": ["explore", "search", "view public profiles"]}
        )


class GetImageView(APIView):
    def post(self, request):
        serializer = ImageRetrieveSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        payload = {"filenames": serializer.validated_data["filenames"]}
        image_service_url = f"{settings.IMAGE_SERVICE_URL}/get"
        return call_image_service(image_service_url, payload)


class HealthCheckView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class UserDetailForAuthView(APIView):
    permission_classes = [permissions.AllowAny]  # Allow Express to access this

    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
            return Response(
                {
                    "id": user.id,
                    "username": user.username,
                    "passwordHash": user.password,  # Django stores hashed password
                    "roles": ["user"],
                }
            )
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND,
            )


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response(
                {"error": "Missing credentials"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            auth_service_response = requests.post(
                f"{settings.EXPRESS_AUTH_URL}/login",
                json={"username": username, "password": password},
            )
            auth_service_response.raise_for_status()
            return Response(
                auth_service_response.json(),
                status=status.HTTP_200_OK,
            )
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )


class ExpressPingView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        payload = {"username": "trong", "password": "cs361"}
        try:
            auth_service_response = requests.post(
                f"{settings.EXPRESS_AUTH_URL}/login",
                json=payload,
            )
            auth_service_response.raise_for_status()
            return Response(
                auth_service_response.json(),
                status=status.HTTP_200_OK,
            )
        except requests.exceptions.RequestException:
            return Response(
                {"error": "Express login failed"},
                status=status.HTTP_502_BAD_GATEWAY,
            )
