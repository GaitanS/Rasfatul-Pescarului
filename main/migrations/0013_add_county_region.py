from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_update_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='county',
            name='region',
            field=models.CharField(max_length=100, default=''),
            preserve_default=False,
        ),
    ]