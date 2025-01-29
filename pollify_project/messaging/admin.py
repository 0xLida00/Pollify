from django.contrib import admin
from .models import Message

class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'sent_at', 'is_read')
    search_fields = ('sender__username', 'recipient__username', 'subject')
    list_filter = ('is_read', 'sent_at')

admin.site.register(Message, MessageAdmin)