from django import forms
from django.contrib.auth import get_user_model
from django.db.models import Value, CharField
from django.db.models.functions import Lower
from .models import Message

# Get the custom user model
User = get_user_model()

class ComposeMessageForm(forms.ModelForm):
    recipient = forms.ModelChoiceField(
        queryset=User.objects.all().annotate(
            lowercase_username=Lower('username')  # Case-insensitive sort key
        ).order_by('lowercase_username'),
        label='Recipient',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        super().__init__(*args, **kwargs)
        if sender:
            # Exclude sender from the list and sort alphabetically in a case-insensitive way
            self.fields['recipient'].queryset = User.objects.exclude(
                id=sender.id
            ).annotate(lowercase_username=Lower('username')).order_by('lowercase_username')