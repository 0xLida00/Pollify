from django.contrib import admin
from .models import Notification

class NotificationAdmin(admin.ModelAdmin):
    list_display = ('recipient', 'actor', 'verb', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('recipient__username', 'actor__username', 'verb')

admin.site.register(Notification, NotificationAdmin)