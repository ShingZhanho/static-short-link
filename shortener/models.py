from django.db import models
from django.utils import timezone


class ShortLink(models.Model):
    """Model for storing short links and their destinations."""
    
    JUMP_TYPE_CHOICES = [
        ('simple', 'Simple Jump - Ignore parameters'),
        ('forward', 'Parameter Forward - Forward all parameters'),
        ('prefix', 'Prefix Mode - Match paths with this prefix'),
        ('prefix-forward', 'Prefix + Forward - Match prefix and forward parameters'),
    ]
    
    slug = models.CharField(
        max_length=255,
        unique=True,
        help_text="The path after /go/ (can include slashes, e.g., 'google' or 'social/twitter')"
    )
    destination_url = models.CharField(
        max_length=2048,
        help_text="The destination URL or URI (supports http://, https://, mailto:, tel:, and custom app protocols)"
    )
    jump_type = models.CharField(
        max_length=20,
        choices=JUMP_TYPE_CHOICES,
        default='simple',
        help_text="Simple: ignore URL parameters. Forward: pass parameters to destination. Prefix: match paths with prefix. Prefix-Forward: combine prefix matching with parameter forwarding"
    )
    description = models.TextField(
        blank=True,
        help_text="Optional description for this short link"
    )
    click_count = models.IntegerField(
        default=0,
        help_text="Number of times this link has been clicked"
    )
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(
        default=True,
        help_text="Inactive links will return 404"
    )
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Short Link'
        verbose_name_plural = 'Short Links'
    
    def __str__(self):
        return f"/go/{self.slug} → {self.destination_url}"
    
    def increment_clicks(self):
        """Increment the click counter."""
        self.click_count += 1
        self.save(update_fields=['click_count'])
    
    @property
    def short_url(self):
        """Return the short URL path."""
        return f"/go/{self.slug}"
