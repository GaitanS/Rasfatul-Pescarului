from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_add_lake_location_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='bank_transfer_ref',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]