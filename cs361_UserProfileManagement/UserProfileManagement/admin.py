from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, UploadedFile, UploadedImage

# Register your models here.
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (None, {'fields': ('bio', 'avatar')}),
    )

admin.site.register(UploadedFile)
admin.site.register(UploadedImage)