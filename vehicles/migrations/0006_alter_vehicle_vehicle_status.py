# Generated by Django 5.1.1 on 2024-09-30 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0005_alter_vehicle_vehicle_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicle',
            name='vehicle_status',
            field=models.CharField(choices=[('Available', 'Available'), ('In Use', 'In Use')], default='Available', max_length=20),
        ),
    ]
