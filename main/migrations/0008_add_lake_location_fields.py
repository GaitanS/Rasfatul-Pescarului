from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_add_lake_fields'),
    ]

    operations = [
        migrations.AddField(
            model_name='lake',
            name='location',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lake',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lake',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=0, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='lake',
            name='image',
            field=models.ImageField(default='', upload_to='lakes/'),
            preserve_default=False,
        ),
    ]