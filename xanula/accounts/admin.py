from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_student', 'is_admin', 'is_staff')
    list_filter = ('is_student', 'is_admin', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_student', 'is_admin')}),
    )

admin.site.register(User, CustomUserAdmin)