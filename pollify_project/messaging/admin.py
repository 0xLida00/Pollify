from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at', 'is_read')
    search_fields = ('subject', 'body')
    list_filter = ('is_read', 'sent_at')