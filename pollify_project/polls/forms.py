from django import forms
from .models import Poll, Choice, Vote


class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ["question", "description", "category", "expires_at"]
        widgets = {
            "question": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter poll question"}),
            "description": forms.Textarea(attrs={"class": "form-control", "placeholder": "Add a description (optional)"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "expires_at": forms.DateTimeInput(attrs={"class": "form-control", "type": "datetime-local"}),
        }

    choices = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control",
                "placeholder": "Enter each choice on a new line",
                "rows": 5,
            }
        ),
        help_text="Enter at least two choices, each on a new line.",
        required=True,
    )


class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["choice_text"]
        widgets = {
            "choice_text": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter choice text"}),
        }


class VoteForm(forms.ModelForm):
    class Meta:
        model = Vote
        fields = ["choice"]
        widgets = {
            "choice": forms.RadioSelect(),
        }