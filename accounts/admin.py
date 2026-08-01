from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, Favorite

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('email', 'username', 'is_vendor', 'is_staff')
    list_filter = ('is_vendor', 'is_staff')

admin.site.register(User, CustomUserAdmin)
admin.site.register(Favorite)