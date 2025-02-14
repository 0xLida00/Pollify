from django import forms
from django.contrib.auth import get_user_model
from django.db.models.functions import Lower
from .models import Message

User = get_user_model()

class ComposeMessageForm(forms.ModelForm):
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all().annotate(
            lowercase_username=Lower('username')
        ).order_by('lowercase_username'),
        label='Recipients',
        widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Message
        fields = ['recipients', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        sender = kwargs.pop('sender', None)
        super().__init__(*args, **kwargs)
        if sender:
            self.fields['recipients'].queryset = User.objects.exclude(id=sender.id)