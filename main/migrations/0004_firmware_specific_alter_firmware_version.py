# Generated by Django 4.2.7 on 2024-06-11 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_alter_firmware_car_model'),
    ]

    operations = [
        migrations.AddField(
            model_name='firmware',
            name='specific',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='firmware',
            name='version',
            field=models.CharField(max_length=5),
        ),
    ]
