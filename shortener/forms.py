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
        
        # Check for invalid characters
        if any(char in slug for char in ['?', '#', '&', ' ']):
            raise forms.ValidationError(
                'Slug cannot contain spaces, ?, #, or & characters'
            )
        
        # Remove leading slash
        slug = slug.lstrip('/')
        
        return slug
    
    def clean(self):
        """Cross-field validation."""
        cleaned_data = super().clean()
        slug = cleaned_data.get('slug')
        jump_type = cleaned_data.get('jump_type')
        
        if slug and jump_type:
            # For prefix modes, ensure slug ends with /
            if jump_type in ['prefix', 'prefix-forward']:
                if not slug.endswith('/'):
                    raise forms.ValidationError({
                        'slug': 'Prefix mode slugs must end with a slash (e.g., "my-prefix/")'
                    })
            # For non-prefix modes, ensure slug does NOT end with /
            else:
                if slug.endswith('/'):
                    cleaned_data['slug'] = slug.rstrip('/')
        
        return cleaned_data
    
    def clean_destination_url(self):
        """Ensure URL has a scheme."""
        url = self.cleaned_data['destination_url']
        
        if not url.startswith(('http://', 'https://')):
            raise forms.ValidationError(
                'URL must start with http:// or https://'
            )
        
        return url
