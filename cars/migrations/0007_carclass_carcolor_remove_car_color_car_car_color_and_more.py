# Generated by Django 4.2.7 on 2024-06-23 11:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0006_car_car_class_car_color_carmodel_horsepower_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarClass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=1)),
            ],
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hex_code', models.CharField(max_length=7)),
            ],
        ),
        migrations.RemoveField(
            model_name='car',
            name='color',
        ),
        migrations.AddField(
            model_name='car',
            name='car_color',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.carcolor'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='available_colors',
            field=models.ManyToManyField(blank=True, to='cars.carcolor'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='classes',
            field=models.ManyToManyField(blank=True, to='cars.carclass'),
        ),
        migrations.AlterField(
            model_name='car',
            name='car_class',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cars.carclass'),
        ),
    ]
