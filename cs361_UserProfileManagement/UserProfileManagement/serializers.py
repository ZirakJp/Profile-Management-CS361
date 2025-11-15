from rest_framework import serializers
from .models import User, UploadedFile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'avatar']

class FileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['id', 'file', 'uploaded_at']

# If using Flask for ImageUpload
class ImageUploadSerializer(serializers.Serializer):
    file = serializers.ImageField()

class ImageRetrieveSerializer(serializers.Serializer):
    filenames = serializers.ListField(
        child=serializers.CharField(), allow_empty=False
    )
