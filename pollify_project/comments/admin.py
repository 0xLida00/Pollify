from django.contrib import admin
from .models import Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = ('poll', 'author', 'created_at')
    search_fields = ('author__username', 'poll__question', 'content')
    list_filter = ('created_at',)

admin.site.register(Comment, CommentAdmin)