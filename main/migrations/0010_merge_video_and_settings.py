from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_add_order_bank_transfer_ref'),
    ]

    operations = [
        # Video model updates
        migrations.AddField(
            model_name='video',
            name='embed_url',
            field=models.URLField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='video',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='video',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
        
        # Site Settings model
        migrations.CreateModel(
            name='SiteSettings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contact_email', models.EmailField(help_text='Email address where contact form messages will be sent', max_length=254)),
                ('company_email', models.EmailField(help_text='Company email displayed on the website', max_length=254)),
                ('company_phone', models.CharField(help_text='Company phone number', max_length=20)),
                ('company_address', models.CharField(help_text='Company address', max_length=200)),
            ],
            options={
                'verbose_name': 'Site Settings',
                'verbose_name_plural': 'Site Settings',
            },
        ),
    ]