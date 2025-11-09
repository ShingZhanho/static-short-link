from django import forms
from .models import ShortLink


class ShortLinkForm(forms.ModelForm):
    class Meta:
        model = ShortLink
        fields = ['slug', 'destination_url', 'jump_type', 'description', 'is_active']
        widgets = {
            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g., google or social/twitter',
            }),
            'destination_url': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com',
            }),
            'jump_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description...',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
    
    def clean_slug(self):
        """Validate slug format."""
        slug = self.cleaned_data['slug']
        
        # Remove leading/trailing slashes
        slug = slug.strip('/')
        
        # Check for invalid characters
        if any(char in slug for char in ['?', '#', '&', ' ']):
            raise forms.ValidationError(
                'Slug cannot contain spaces, ?, #, or & characters'
            )
        
        return slug
    
    def clean_destination_url(self):
        """Ensure URL has a scheme."""
        url = self.cleaned_data['destination_url']
        
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError(
                'URL must start with http:// or https://'
            )
        
        return url
