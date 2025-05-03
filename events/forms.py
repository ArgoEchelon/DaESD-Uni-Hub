from django import forms
from .models import Event
from communities.models import Tag

class EventForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. music, volunteering, cs'})
    )

    class Meta:
        model = Event
        fields = ['title', 'description', 'location', 'start_time', 'end_time', 'tags']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
