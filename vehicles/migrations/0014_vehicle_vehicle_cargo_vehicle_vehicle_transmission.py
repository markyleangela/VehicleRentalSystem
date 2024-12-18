# Generated by Django 5.1.1 on 2024-10-31 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0013_vehicle_vehicle_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_cargo',
            field=models.CharField(choices=[('Standard Cargo Capacity', '12.6 cu ft'), ('Expanded Cargo Capacity', ' 38.5 cu ft'), ('Max Cargo Capacity', '75.5 cu ft ')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_transmission',
            field=models.CharField(choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')], max_length=50, null=True),
        ),
    ]
