from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_add_category_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='lake',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='lake',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='lake',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]