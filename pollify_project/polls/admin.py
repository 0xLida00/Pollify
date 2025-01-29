from django.contrib import admin
from .models import Poll, Choice, Vote

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2  # Provides extra fields for adding choices when creating a poll

class PollAdmin(admin.ModelAdmin):
    list_display = ('question', 'author', 'created_at', 'expires_at')
    search_fields = ('question', 'author__username')
    list_filter = ('created_at', 'expires_at')
    inlines = [ChoiceInline]

class VoteAdmin(admin.ModelAdmin):
    list_display = ('poll', 'choice', 'voter', 'voted_at')
    search_fields = ('poll__question', 'voter__username')
    list_filter = ('voted_at',)

admin.site.register(Poll, PollAdmin)
admin.site.register(Choice)
admin.site.register(Vote, VoteAdmin)