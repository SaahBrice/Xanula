from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin


# Register your models here.
class CustomUserAdmin(UserAdmin):

    list_filter = ('is_student', 'is_admin', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        ('Custom Fields', {'fields': ('is_student', 'is_admin')}),
    )
    list_display = ('username', 'email', 'is_staff', 'is_active', 'has_active_subscription')
    
    def has_active_subscription(self, obj):
        return obj.has_active_subscription()
    has_active_subscription.boolean = True
    has_active_subscription.short_description = 'Active Subscription'

admin.site.register(User, CustomUserAdmin)