# Generated by Django 5.1.1 on 2024-11-05 03:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0005_alter_rentalrecord_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalrecord',
            name='is_rated',
            field=models.BooleanField(default=False),
        ),
    ]
