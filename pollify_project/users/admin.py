from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Follow

# Extend Django's default UserAdmin to customize user display
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_active')
    search_fields = ('username', 'email')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('bio', 'profile_picture')}),
    )

admin.site.register(User, CustomUserAdmin)

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ('follower', 'followed', 'followed_at')
    search_fields = ('follower__username', 'followed__username')