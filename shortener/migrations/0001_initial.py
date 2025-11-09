# Generated migration

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(help_text="The path after /go/ (can include slashes, e.g., 'google' or 'social/twitter')", max_length=255, unique=True)),
                ('destination_url', models.URLField(help_text='The full URL to redirect to (must start with http:// or https://)', max_length=2048)),
                ('jump_type', models.CharField(choices=[('simple', 'Simple Jump - Ignore parameters'), ('forward', 'Parameter Forward - Forward all parameters')], default='simple', help_text='Simple: ignore URL parameters. Forward: pass parameters to destination', max_length=10)),
                ('description', models.TextField(blank=True, help_text='Optional description for this short link')),
                ('click_count', models.IntegerField(default=0, help_text='Number of times this link has been clicked')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, help_text='Inactive links will return 404')),
            ],
            options={
                'verbose_name': 'Short Link',
                'verbose_name_plural': 'Short Links',
                'ordering': ['-created_at'],
            },
        ),
    ]
