from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_add_product_active_fields'),
    ]

    operations = [
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
    ]