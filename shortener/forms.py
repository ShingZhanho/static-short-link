from django import forms
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
import re
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
            'destination_url': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'https://example.com or mailto:email@example.com or tel:+1234567890',
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
        """Validate URL/URI format - allow various protocols."""
        url = self.cleaned_data['destination_url'].strip()
        
        # Check if it has a protocol/scheme
        if not re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:', url):
            raise forms.ValidationError(
                'Destination must include a protocol (e.g., https://, mailto:, tel:, or custom app protocol)'
            )
        
        # For HTTP/HTTPS, do standard validation
        if url.startswith(('http://', 'https://')):
            validator = URLValidator(schemes=['http', 'https'])
            try:
                validator(url)
            except ValidationError:
                raise forms.ValidationError('Invalid HTTP/HTTPS URL format')
        
        # For mailto:, do basic validation
        elif url.startswith('mailto:'):
            email_part = url[7:]  # Remove 'mailto:'
            if not email_part or '@' not in email_part.split('?')[0]:
                raise forms.ValidationError('Invalid mailto: format. Example: mailto:user@example.com')
        
        # For tel:, do basic validation
        elif url.startswith('tel:'):
            phone_part = url[4:]  # Remove 'tel:'
            if not phone_part or not re.match(r'^[0-9+\-() ]+$', phone_part):
                raise forms.ValidationError('Invalid tel: format. Example: tel:+1234567890')
        
        # For other protocols (custom apps, etc.), just ensure it's not empty after the colon
        else:
            protocol, _, content = url.partition(':')
            if not content:
                raise forms.ValidationError(f'Invalid {protocol}: URI - missing content after protocol')
        
        return url
