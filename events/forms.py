from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g. seminar, AI, networking'
        })
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_time', 'end_time', 'tags']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }
