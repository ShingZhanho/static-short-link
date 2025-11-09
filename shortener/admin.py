from django.contrib import admin
from .models import ShortLink


@admin.register(ShortLink)
class ShortLinkAdmin(admin.ModelAdmin):
    list_display = ['slug', 'destination_url', 'jump_type', 'click_count', 'is_active', 'created_at']
    list_filter = ['jump_type', 'is_active', 'created_at']
    search_fields = ['slug', 'destination_url', 'description']
    readonly_fields = ['click_count', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Short Link Configuration', {
            'fields': ('slug', 'destination_url', 'jump_type', 'is_active')
        }),
        ('Details', {
            'fields': ('description',)
        }),
        ('Statistics', {
            'fields': ('click_count', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
