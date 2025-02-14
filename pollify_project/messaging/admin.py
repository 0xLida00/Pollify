from django.contrib import admin
from .models import Message

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'list_recipients', 'subject', 'sent_at', 'is_read')
    search_fields = ('subject', 'body', 'sender__username', 'recipients__username')
    list_filter = ('is_read', 'sent_at')

    def list_recipients(self, obj):
        """Display recipients as a comma-separated list."""
        return ", ".join([user.username for user in obj.recipients.all()])

    list_recipients.short_description = 'Recipients'