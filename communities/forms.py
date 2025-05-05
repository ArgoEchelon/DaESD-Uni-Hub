from django import forms
from .models import Community

class CommunityForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        label="Tags (comma-separated)",
        widget=forms.TextInput(attrs={'placeholder': 'e.g. tech, ai, student'})
    )

    class Meta:
        model = Community
        fields = ['name', 'description', 'image', 'tags']

    def __init__(self, *args, **kwargs):
        # Handle initial display of tags as comma-separated names
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.setdefault('initial', {})
            initial['tags'] = ', '.join(tag.name for tag in instance.tags.all())
        super().__init__(*args, **kwargs)
