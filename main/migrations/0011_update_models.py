from django.db import migrations, models
from django.utils import timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_merge_video_and_settings'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, help_text='Profile picture', null=True, upload_to='avatars/'),
        ),
        migrations.AddField(
            model_name='profile',
            name='is_email_verified',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='email_verification_token',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]