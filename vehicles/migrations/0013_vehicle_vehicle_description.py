# Generated by Django 5.1.1 on 2024-10-31 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0012_alter_vehicle_vehicle_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='vehicle_description',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
