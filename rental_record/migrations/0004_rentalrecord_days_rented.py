# Generated by Django 5.1.1 on 2024-10-31 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rental_record', '0003_alter_rentalrecord_rental_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='rentalrecord',
            name='days_rented',
            field=models.IntegerField(default=0),
        ),
    ]
